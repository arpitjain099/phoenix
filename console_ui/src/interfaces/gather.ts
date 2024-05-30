import { JobRunResponse } from "./job-run";

export interface GatherResponse {
	description: string;
	id: number;
	platform: string;
	data_type: string;
	source: string;
	created_at: string;
	updated_at: string;
	project_id: number;
	deleted_at: string;
	latest_job_run: JobRunResponse;
}
