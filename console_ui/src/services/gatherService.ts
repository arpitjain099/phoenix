/* eslint-disable class-methods-use-this */
import axios from "@providers/data-provider/axios";
import { IGatherRun } from "src/interfaces/gather";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default class GatherService {
	async getGatherRunEstimate(data: IGatherRun) {
		const response = await axios.get(
			`${API_URL}/projects/${data?.project_id}/gathers/${data?.gather_id}/estimate`
		);
		return response;
	}

	async gatherRun(data: IGatherRun) {
		const response = await axios.post(
			`${API_URL}/projects/${data?.project_id}/gathers/${data?.gather_id}/runs`
		);
		return response;
	}
}
