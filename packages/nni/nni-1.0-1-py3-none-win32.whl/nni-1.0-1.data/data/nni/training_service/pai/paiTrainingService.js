'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const path = require("path");
const request = require("request");
const component = require("../../common/component");
const events_1 = require("events");
const ts_deferred_1 = require("ts-deferred");
const typescript_string_operations_1 = require("typescript-string-operations");
const experimentStartupInfo_1 = require("../../common/experimentStartupInfo");
const log_1 = require("../../common/log");
const utils_1 = require("../../common/utils");
const containerJobData_1 = require("../common/containerJobData");
const trialConfigMetadataKey_1 = require("../common/trialConfigMetadataKey");
const util_1 = require("../common/util");
const hdfsClientUtility_1 = require("./hdfsClientUtility");
const paiConfig_1 = require("./paiConfig");
const paiData_1 = require("./paiData");
const paiJobInfoCollector_1 = require("./paiJobInfoCollector");
const paiJobRestServer_1 = require("./paiJobRestServer");
const WebHDFS = require("webhdfs");
let PAITrainingService = class PAITrainingService {
    constructor() {
        this.stopping = false;
        this.versionCheck = true;
        this.isMultiPhase = false;
        this.authFileHdfsPath = undefined;
        this.log = log_1.getLogger();
        this.metricsEmitter = new events_1.EventEmitter();
        this.trialJobsMap = new Map();
        this.jobQueue = [];
        this.expRootDir = path.join('/nni', 'experiments', experimentStartupInfo_1.getExperimentId());
        this.experimentId = experimentStartupInfo_1.getExperimentId();
        this.paiJobCollector = new paiJobInfoCollector_1.PAIJobInfoCollector(this.trialJobsMap);
        this.nextTrialSequenceId = -1;
        this.paiTokenUpdateInterval = 7200000;
        this.logCollection = 'none';
        this.log.info('Construct OpenPAI training service.');
    }
    async run() {
        this.log.info('Run PAI training service.');
        const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
        await restServer.start();
        restServer.setEnableVersionCheck = this.versionCheck;
        this.log.info(`PAI Training service rest server listening on: ${restServer.endPoint}`);
        await Promise.all([
            this.statusCheckingLoop(),
            this.submitJobLoop()
        ]);
        this.log.info('PAI training service exit.');
    }
    async listTrialJobs() {
        const jobs = [];
        for (const [key, value] of this.trialJobsMap) {
            if (value.form.jobType === 'TRIAL') {
                jobs.push(await this.getTrialJob(key));
            }
        }
        return Promise.resolve(jobs);
    }
    async getTrialJob(trialJobId) {
        if (this.paiClusterConfig === undefined) {
            throw new Error('PAI Cluster config is not initialized');
        }
        const paiTrialJob = this.trialJobsMap.get(trialJobId);
        if (paiTrialJob === undefined) {
            return Promise.reject(`trial job ${trialJobId} not found`);
        }
        return Promise.resolve(paiTrialJob);
    }
    addTrialJobMetricListener(listener) {
        this.metricsEmitter.on('metric', listener);
    }
    removeTrialJobMetricListener(listener) {
        this.metricsEmitter.off('metric', listener);
    }
    async submitTrialJob(form) {
        if (this.paiClusterConfig === undefined) {
            throw new Error(`paiClusterConfig not initialized!`);
        }
        const deferred = new ts_deferred_1.Deferred();
        this.log.info(`submitTrialJob: form: ${JSON.stringify(form)}`);
        const trialJobId = utils_1.uniqueString(5);
        const trialSequenceId = this.generateSequenceId();
        const trialWorkingFolder = path.join(this.expRootDir, 'trials', trialJobId);
        const paiJobName = `nni_exp_${this.experimentId}_trial_${trialJobId}`;
        const hdfsCodeDir = hdfsClientUtility_1.HDFSClientUtility.getHdfsTrialWorkDir(this.paiClusterConfig.userName, trialJobId);
        const hdfsOutputDir = utils_1.unixPathJoin(hdfsCodeDir, 'nnioutput');
        const hdfsLogPath = typescript_string_operations_1.String.Format(paiData_1.PAI_LOG_PATH_FORMAT, this.paiClusterConfig.host, hdfsOutputDir);
        const trialJobDetail = new paiData_1.PAITrialJobDetail(trialJobId, 'WAITING', paiJobName, Date.now(), trialWorkingFolder, form, trialSequenceId, hdfsLogPath);
        this.trialJobsMap.set(trialJobId, trialJobDetail);
        this.jobQueue.push(trialJobId);
        deferred.resolve(trialJobDetail);
        return deferred.promise;
    }
    async updateTrialJob(trialJobId, form) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`updateTrialJob failed: ${trialJobId} not found`);
        }
        if (form.jobType === 'TRIAL') {
            await this.writeParameterFile(trialJobId, form.hyperParameters);
        }
        else {
            throw new Error(`updateTrialJob failed: jobType ${form.jobType} not supported.`);
        }
        return trialJobDetail;
    }
    get isMultiPhaseJobSupported() {
        return true;
    }
    cancelTrialJob(trialJobId, isEarlyStopped = false) {
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        const deferred = new ts_deferred_1.Deferred();
        if (trialJobDetail === undefined) {
            this.log.error(`cancelTrialJob: trial job id ${trialJobId} not found`);
            return Promise.reject();
        }
        if (this.paiClusterConfig === undefined) {
            throw new Error('PAI Cluster config is not initialized');
        }
        if (this.paiToken === undefined) {
            throw new Error('PAI token is not initialized');
        }
        const stopJobRequest = {
            uri: `http://${this.paiClusterConfig.host}/rest-server/api/v1/user/${this.paiClusterConfig.userName}\
/jobs/${trialJobDetail.paiJobName}/executionType`,
            method: 'PUT',
            json: true,
            body: { value: 'STOP' },
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.paiToken}`
            }
        };
        trialJobDetail.isEarlyStopped = isEarlyStopped;
        request(stopJobRequest, (error, response, body) => {
            if ((error !== undefined && error !== null) || response.statusCode >= 400) {
                this.log.error(`PAI Training service: stop trial ${trialJobId} to PAI Cluster failed!`);
                deferred.reject((error !== undefined && error !== null) ? error.message :
                    `Stop trial failed, http code: ${response.statusCode}`);
            }
            else {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
    async setClusterMetadata(key, value) {
        const deferred = new ts_deferred_1.Deferred();
        switch (key) {
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.NNI_MANAGER_IP:
                this.nniManagerIpConfig = JSON.parse(value);
                deferred.resolve();
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.PAI_CLUSTER_CONFIG:
                this.paiClusterConfig = JSON.parse(value);
                this.hdfsClient = WebHDFS.createClient({
                    user: this.paiClusterConfig.userName,
                    port: 80,
                    path: '/webhdfs/api/v1',
                    host: this.paiClusterConfig.host
                });
                await this.updatePaiToken();
                deferred.resolve();
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.TRIAL_CONFIG:
                if (this.paiClusterConfig === undefined) {
                    this.log.error('pai cluster config is not initialized');
                    deferred.reject(new Error('pai cluster config is not initialized'));
                    break;
                }
                this.paiTrialConfig = JSON.parse(value);
                try {
                    await util_1.validateCodeDir(this.paiTrialConfig.codeDir);
                }
                catch (error) {
                    this.log.error(error);
                    deferred.reject(new Error(error));
                    break;
                }
                this.copyExpCodeDirPromise = hdfsClientUtility_1.HDFSClientUtility.copyDirectoryToHdfs(this.paiTrialConfig.codeDir, hdfsClientUtility_1.HDFSClientUtility.getHdfsExpCodeDir(this.paiClusterConfig.userName), this.hdfsClient);
                if (this.paiTrialConfig.authFile) {
                    this.authFileHdfsPath = utils_1.unixPathJoin(hdfsClientUtility_1.HDFSClientUtility.hdfsExpRootDir(this.paiClusterConfig.userName), 'authFile');
                    this.copyAuthFilePromise = hdfsClientUtility_1.HDFSClientUtility.copyFileToHdfs(this.paiTrialConfig.authFile, this.authFileHdfsPath, this.hdfsClient);
                }
                deferred.resolve();
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.VERSION_CHECK:
                this.versionCheck = (value === 'true' || value === 'True');
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.LOG_COLLECTION:
                this.logCollection = value;
                break;
            case trialConfigMetadataKey_1.TrialConfigMetadataKey.MULTI_PHASE:
                this.isMultiPhase = (value === 'true' || value === 'True');
                break;
            default:
                throw new Error(`Uknown key: ${key}`);
        }
        return deferred.promise;
    }
    getClusterMetadata(key) {
        const deferred = new ts_deferred_1.Deferred();
        deferred.resolve();
        return deferred.promise;
    }
    async cleanUp() {
        this.log.info('Stopping PAI training service...');
        this.stopping = true;
        const deferred = new ts_deferred_1.Deferred();
        const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
        try {
            await restServer.stop();
            deferred.resolve();
            this.log.info('PAI Training service rest server stopped successfully.');
        }
        catch (error) {
            this.log.error(`PAI Training service rest server stopped failed, error: ${error.message}`);
            deferred.reject(error);
        }
        return deferred.promise;
    }
    get MetricsEmitter() {
        return this.metricsEmitter;
    }
    async submitTrialJobToPAI(trialJobId) {
        const deferred = new ts_deferred_1.Deferred();
        const trialJobDetail = this.trialJobsMap.get(trialJobId);
        if (trialJobDetail === undefined) {
            throw new Error(`Failed to find PAITrialJobDetail for job ${trialJobId}`);
        }
        if (this.paiClusterConfig === undefined) {
            throw new Error('PAI Cluster config is not initialized');
        }
        if (this.paiTrialConfig === undefined) {
            throw new Error('trial config is not initialized');
        }
        if (this.paiToken === undefined) {
            throw new Error('PAI token is not initialized');
        }
        if (this.paiRestServerPort === undefined) {
            const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
            this.paiRestServerPort = restServer.clusterRestServerPort;
        }
        if (this.copyExpCodeDirPromise !== undefined) {
            await this.copyExpCodeDirPromise;
        }
        if (this.paiTrialConfig.authFile) {
            await this.copyAuthFilePromise;
        }
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        await util_1.execMkdir(trialLocalTempFolder);
        const runScriptContent = containerJobData_1.CONTAINER_INSTALL_NNI_SHELL_FORMAT;
        await fs.promises.writeFile(path.join(trialLocalTempFolder, 'install_nni.sh'), runScriptContent, { encoding: 'utf8' });
        const trialForm = trialJobDetail.form;
        if (trialForm !== undefined) {
            await fs.promises.writeFile(path.join(trialLocalTempFolder, utils_1.generateParamFileName(trialForm.hyperParameters)), trialForm.hyperParameters.value, { encoding: 'utf8' });
        }
        const hdfsCodeDir = hdfsClientUtility_1.HDFSClientUtility.getHdfsTrialWorkDir(this.paiClusterConfig.userName, trialJobId);
        const hdfsOutputDir = utils_1.unixPathJoin(hdfsCodeDir, 'nnioutput');
        const nniManagerIp = this.nniManagerIpConfig ? this.nniManagerIpConfig.nniManagerIp : utils_1.getIPV4Address();
        const version = this.versionCheck ? await utils_1.getVersion() : '';
        const nniPaiTrialCommand = typescript_string_operations_1.String.Format(paiData_1.PAI_TRIAL_COMMAND_FORMAT, `$PWD/${trialJobId}`, `$PWD/${trialJobId}/nnioutput`, trialJobId, this.experimentId, trialJobDetail.sequenceId, this.isMultiPhase, this.paiTrialConfig.command, nniManagerIp, this.paiRestServerPort, hdfsOutputDir, this.paiClusterConfig.host, this.paiClusterConfig.userName, hdfsClientUtility_1.HDFSClientUtility.getHdfsExpCodeDir(this.paiClusterConfig.userName), version, this.logCollection)
            .replace(/\r\n|\n|\r/gm, '');
        console.log(`nniPAItrial command is ${nniPaiTrialCommand.trim()}`);
        const paiTaskRoles = [
            new paiConfig_1.PAITaskRole(`nni_trail_${trialJobId}`, 1, this.paiTrialConfig.cpuNum, this.paiTrialConfig.memoryMB, this.paiTrialConfig.gpuNum, nniPaiTrialCommand, this.paiTrialConfig.shmMB, this.paiTrialConfig.portList)
        ];
        const paiJobConfig = new paiConfig_1.PAIJobConfig(trialJobDetail.paiJobName, this.paiTrialConfig.image, `$PAI_DEFAULT_FS_URI${hdfsCodeDir}`, paiTaskRoles, this.paiTrialConfig.virtualCluster === undefined ? 'default' : this.paiTrialConfig.virtualCluster.toString(), this.authFileHdfsPath);
        try {
            await hdfsClientUtility_1.HDFSClientUtility.copyDirectoryToHdfs(trialLocalTempFolder, hdfsCodeDir, this.hdfsClient);
        }
        catch (error) {
            this.log.error(`PAI Training service: copy ${this.paiTrialConfig.codeDir} to HDFS ${hdfsCodeDir} failed, error is ${error}`);
            trialJobDetail.status = 'FAILED';
            deferred.resolve(true);
            return deferred.promise;
        }
        const submitJobRequest = {
            uri: `http://${this.paiClusterConfig.host}/rest-server/api/v1/user/${this.paiClusterConfig.userName}/jobs`,
            method: 'POST',
            json: true,
            body: paiJobConfig,
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.paiToken}`
            }
        };
        request(submitJobRequest, (error, response, body) => {
            if ((error !== undefined && error !== null) || response.statusCode >= 400) {
                const errorMessage = (error !== undefined && error !== null) ? error.message :
                    `Submit trial ${trialJobId} failed, http code:${response.statusCode}, http body: ${response.body}`;
                this.log.error(errorMessage);
                trialJobDetail.status = 'FAILED';
                deferred.resolve(true);
            }
            else {
                trialJobDetail.submitTime = Date.now();
                deferred.resolve(true);
            }
        });
        return deferred.promise;
    }
    generateSequenceId() {
        if (this.nextTrialSequenceId === -1) {
            this.nextTrialSequenceId = experimentStartupInfo_1.getInitTrialSequenceId();
        }
        return this.nextTrialSequenceId++;
    }
    async statusCheckingLoop() {
        while (!this.stopping) {
            try {
                await this.updatePaiToken();
            }
            catch (error) {
                this.log.error(`${error}`);
                if (this.paiToken === undefined) {
                    throw new Error(error);
                }
            }
            await this.paiJobCollector.retrieveTrialStatus(this.paiToken, this.paiClusterConfig);
            const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
            if (restServer.getErrorMessage !== undefined) {
                throw new Error(restServer.getErrorMessage);
            }
            await utils_1.delay(3000);
        }
    }
    async submitJobLoop() {
        while (!this.stopping) {
            while (!this.stopping && this.jobQueue.length > 0) {
                const trialJobId = this.jobQueue[0];
                if (await this.submitTrialJobToPAI(trialJobId)) {
                    this.jobQueue.shift();
                }
                else {
                    break;
                }
            }
            await utils_1.delay(3000);
        }
    }
    async updatePaiToken() {
        const deferred = new ts_deferred_1.Deferred();
        const currentTime = new Date().getTime();
        if (this.paiTokenUpdateTime !== undefined && (currentTime - this.paiTokenUpdateTime) < this.paiTokenUpdateInterval) {
            return Promise.resolve();
        }
        if (this.paiClusterConfig === undefined) {
            const paiClusterConfigError = `pai cluster config not initialized!`;
            this.log.error(`${paiClusterConfigError}`);
            throw Error(`${paiClusterConfigError}`);
        }
        const authenticationReq = {
            uri: `http://${this.paiClusterConfig.host}/rest-server/api/v1/token`,
            method: 'POST',
            json: true,
            body: {
                username: this.paiClusterConfig.userName,
                password: this.paiClusterConfig.passWord
            }
        };
        request(authenticationReq, (error, response, body) => {
            if (error !== undefined && error !== null) {
                this.log.error(`Get PAI token failed: ${error.message}`);
                deferred.reject(new Error(`Get PAI token failed: ${error.message}`));
            }
            else {
                if (response.statusCode !== 200) {
                    this.log.error(`Get PAI token failed: get PAI Rest return code ${response.statusCode}`);
                    deferred.reject(new Error(`Get PAI token failed: ${response.body}, please check paiConfig username or password`));
                }
                this.paiToken = body.token;
                this.paiTokenUpdateTime = new Date().getTime();
                deferred.resolve();
            }
        });
        let timeoutId;
        const timeoutDelay = new Promise((resolve, reject) => {
            timeoutId = setTimeout(() => reject(new Error('Get PAI token timeout. Please check your PAI cluster.')), 5000);
        });
        return Promise.race([timeoutDelay, deferred.promise])
            .finally(() => { clearTimeout(timeoutId); });
    }
    async writeParameterFile(trialJobId, hyperParameters) {
        if (this.paiClusterConfig === undefined) {
            throw new Error('PAI Cluster config is not initialized');
        }
        if (this.paiTrialConfig === undefined) {
            throw new Error('PAI trial config is not initialized');
        }
        const trialLocalTempFolder = path.join(utils_1.getExperimentRootDir(), 'trials-local', trialJobId);
        const hpFileName = utils_1.generateParamFileName(hyperParameters);
        const localFilepath = path.join(trialLocalTempFolder, hpFileName);
        await fs.promises.writeFile(localFilepath, hyperParameters.value, { encoding: 'utf8' });
        const hdfsCodeDir = hdfsClientUtility_1.HDFSClientUtility.getHdfsTrialWorkDir(this.paiClusterConfig.userName, trialJobId);
        const hdfsHpFilePath = path.join(hdfsCodeDir, hpFileName);
        await hdfsClientUtility_1.HDFSClientUtility.copyFileToHdfs(localFilepath, hdfsHpFilePath, this.hdfsClient);
        await this.postParameterFileMeta({
            experimentId: this.experimentId,
            trialId: trialJobId,
            filePath: hdfsHpFilePath
        });
    }
    postParameterFileMeta(parameterFileMeta) {
        const deferred = new ts_deferred_1.Deferred();
        const restServer = component.get(paiJobRestServer_1.PAIJobRestServer);
        const req = {
            uri: `${restServer.endPoint}${restServer.apiRootUrl}/parameter-file-meta`,
            method: 'POST',
            json: true,
            body: parameterFileMeta
        };
        request(req, (err, res) => {
            if (err) {
                deferred.reject(err);
            }
            else {
                deferred.resolve();
            }
        });
        return deferred.promise;
    }
};
PAITrainingService = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], PAITrainingService);
exports.PAITrainingService = PAITrainingService;
