import { JobRunResponse } from "./job-run";

export interface IClassifierArchiveRestore {
	project_id: number;
	id?: number;
}

export interface ClassifierResponse {
	name: string;
	id: number;
	archived_at: string;
	type: string;
	last_edited_at: string;
	created_at: string;
	updated_at: string;
	project_id: number;
	latest_job_run: JobRunResponse;
	latest_version: {
		classes: any;
		classifier_id: number;
		created_at: string;
		params: any;
		updated_at: string;
		version_id: number;
	};
}

export interface ClassifierPayload {
	name: string;
	description: string;
	intermediatory_classes?: ClassifierClassPayload[];
}

export interface ClassifierClassPayload {
	name: string;
	description: string;
}

export interface AddClassToAuthorPayload {
	class_id: number;
	phoenix_platform_message_author_id: string;
}
