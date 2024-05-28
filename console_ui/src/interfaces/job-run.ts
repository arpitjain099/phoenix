export interface JobRunResponse {
	foreign_id: number;
	foreign_job_type: string;
	id: number;
	created_at: string;
	updated_at: string;
	project_id: number;
	status: string;
	started_processing_at: string;
	completed_at: string;
	flow_run_id: string;
	flow_run_name: string;
}
