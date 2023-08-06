'use strict';
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
const assert = require("assert");
const os = require("os");
const path = require("path");
const component = require("../common/component");
let ExperimentStartupInfo = class ExperimentStartupInfo {
    constructor() {
        this.experimentId = '';
        this.newExperiment = true;
        this.basePort = -1;
        this.initialized = false;
        this.initTrialSequenceID = 0;
        this.logDir = '';
        this.logLevel = '';
    }
    setStartupInfo(newExperiment, experimentId, basePort, logDir, logLevel) {
        assert(!this.initialized);
        assert(experimentId.trim().length > 0);
        this.newExperiment = newExperiment;
        this.experimentId = experimentId;
        this.basePort = basePort;
        this.initialized = true;
        if (logDir !== undefined && logDir.length > 0) {
            this.logDir = path.join(logDir, getExperimentId());
        }
        else {
            this.logDir = path.join(os.homedir(), 'nni', 'experiments', getExperimentId());
        }
        if (logLevel !== undefined && logLevel.length > 1) {
            this.logLevel = logLevel;
        }
    }
    getExperimentId() {
        assert(this.initialized);
        return this.experimentId;
    }
    getBasePort() {
        assert(this.initialized);
        return this.basePort;
    }
    isNewExperiment() {
        assert(this.initialized);
        return this.newExperiment;
    }
    getLogDir() {
        assert(this.initialized);
        return this.logDir;
    }
    getLogLevel() {
        assert(this.initialized);
        return this.logLevel;
    }
    setInitTrialSequenceId(initSequenceId) {
        assert(this.initialized);
        this.initTrialSequenceID = initSequenceId;
    }
    getInitTrialSequenceId() {
        assert(this.initialized);
        return this.initTrialSequenceID;
    }
};
ExperimentStartupInfo = __decorate([
    component.Singleton
], ExperimentStartupInfo);
exports.ExperimentStartupInfo = ExperimentStartupInfo;
function getExperimentId() {
    return component.get(ExperimentStartupInfo).getExperimentId();
}
exports.getExperimentId = getExperimentId;
function getBasePort() {
    return component.get(ExperimentStartupInfo).getBasePort();
}
exports.getBasePort = getBasePort;
function isNewExperiment() {
    return component.get(ExperimentStartupInfo).isNewExperiment();
}
exports.isNewExperiment = isNewExperiment;
function setInitTrialSequenceId(initSequenceId) {
    component.get(ExperimentStartupInfo).setInitTrialSequenceId(initSequenceId);
}
exports.setInitTrialSequenceId = setInitTrialSequenceId;
function getInitTrialSequenceId() {
    return component.get(ExperimentStartupInfo).getInitTrialSequenceId();
}
exports.getInitTrialSequenceId = getInitTrialSequenceId;
function getExperimentStartupInfo() {
    return component.get(ExperimentStartupInfo);
}
exports.getExperimentStartupInfo = getExperimentStartupInfo;
function setExperimentStartupInfo(newExperiment, experimentId, basePort, logDir, logLevel) {
    component.get(ExperimentStartupInfo)
        .setStartupInfo(newExperiment, experimentId, basePort, logDir, logLevel);
}
exports.setExperimentStartupInfo = setExperimentStartupInfo;
