/* eslint-disable class-methods-use-this */
import axios from "@providers/data-provider/axios";
import { IJobRun } from "src/interfaces/job-run";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default class GatherService {
	async getGatherRunEstimate(data: IJobRun) {
		const response = await axios.get(
			`${API_URL}/projects/${data?.project_id}/gathers/${data?.id}/estimate`
		);
		return response;
	}
}
