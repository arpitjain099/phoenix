/* eslint-disable class-methods-use-this */
import axios from "@providers/data-provider/axios";
import { IJobRun } from "src/interfaces/job-run";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default class JobRunService {
	async jobRun(data: IJobRun) {
		const response = await axios.post(
			`${API_URL}/projects/${data?.project_id}/job_runs/`,
			{
				foreign_id: data.id,
				foreign_job_type: data.type,
			}
		);
		return response;
	}

	async fetchJobRuns(data: IJobRun) {
		const response = await axios.get(
			`${API_URL}/projects/${data?.project_id}/job_runs?foreign_job_type=${data.type}`
		);
		return response;
	}

	async fetchJobRun(data: IJobRun) {
		const response = await axios.get(
			`${API_URL}/projects/${data?.project_id}/job_runs/${data.id}`
		);
		return response;
	}
}
