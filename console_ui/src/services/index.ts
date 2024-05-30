/* eslint-disable import/prefer-default-export */
import JobRunService from "./jobRunService";
import StorageService from "./storageService";

export const storageService = new StorageService();
export const jobRunService = new JobRunService();
