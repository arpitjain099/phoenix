/* eslint-disable import/prefer-default-export */
import GatherService from "./gatherService";
import StorageService from "./storageService";

export const storageService = new StorageService();
export const gatherService = new GatherService();
