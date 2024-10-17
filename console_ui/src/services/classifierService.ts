/* eslint-disable class-methods-use-this */
import axios from "@providers/data-provider/axios";
import { IClassifierArchiveRestore } from "src/interfaces/classifier";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default class ClassifierService {
	async archiveClassifier(data: IClassifierArchiveRestore) {
		const response = await axios.post(
			`${API_URL}/projects/${data?.project_id}/classifiers/${data?.id}/archive`
		);
		return response;
	}

	async restoreClassifier(data: IClassifierArchiveRestore) {
		const response = await axios.post(
			`${API_URL}/projects/${data?.project_id}/classifiers/${data?.id}/restore`
		);
		return response;
	}
}
