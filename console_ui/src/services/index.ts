/* eslint-disable import/prefer-default-export */
import ClassifierService from "./classifierService";
import GatherService from "./gatherService";
import JobRunService from "./jobRunService";
import StorageService from "./storageService";

export const storageService = new StorageService();
export const jobRunService = new JobRunService();
export const gatherService = new GatherService();
export const classifierService = new ClassifierService();
