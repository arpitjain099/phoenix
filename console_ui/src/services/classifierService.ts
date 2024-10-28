/* eslint-disable class-methods-use-this */
import axios from "@providers/data-provider/axios";
import {
	ClassifierClassPayload,
	ClassifierPayload,
	IClassifierArchiveRestore,
} from "src/interfaces/classifier";

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

	async getClassifierData(params: {
		project_id: string;
		classifier_id: string;
	}) {
		const response = await axios.get(
			`${API_URL}/projects/${params?.project_id}/classifiers/${params?.classifier_id}`
		);
		return response;
	}

	async runKeywordClassifier(params: any) {
		const response = await axios.post(
			`${API_URL}/projects/${params?.project_id}/classifiers/keyword_match/${params?.classifier_id}/version_and_run`
		);
		return response;
	}

	async updateClassifierBasicData(params: any, data: ClassifierPayload) {
		const response = await axios.patch(
			`${API_URL}/projects/${params?.project_id}/classifiers/${params?.classifier_id}`,
			data
		);
		return response;
	}

	async createKeywordClassifier(params: any, data: ClassifierPayload) {
		const response = await axios.post(
			`${API_URL}/projects/${params?.project_id}/classifiers/keyword_match`,
			data
		);
		return response;
	}

	async createClassifierClassData(params: any, data: ClassifierClassPayload) {
		const response = await axios.post(
			`${API_URL}/projects/${params?.project_id}/classifiers/${params?.classifier_id}/intermediatory_classes`,
			data
		);
		return response;
	}

	async updateClassifierClassData(params: any, data: ClassifierClassPayload) {
		const response = await axios.patch(
			`${API_URL}/projects/${params?.project_id}/classifiers/${params?.classifier_id}/intermediatory_classes/${params?.class_id}`,
			data
		);
		return response;
	}

	async removeClassifierClassData(params: any) {
		const response = await axios.delete(
			`${API_URL}/projects/${params?.project_id}/classifiers/${params?.classifier_id}/intermediatory_classes/${params?.class_id}`
		);
		return response;
	}

	async createKeywordClassifierConfig(
		params: any,
		data: { class_id: number; musts: string; nots: string }
	) {
		const response = await axios.post(
			`${API_URL}/projects/${params?.project_id}/classifiers/keyword_match/${params?.classifier_id}/intermediatory_class_to_keyword_configs`,
			data
		);
		return response;
	}

	async updateKeywordClassifierConfig(
		params: any,
		data: { musts: string; nots: string }
	) {
		const response = await axios.patch(
			`${API_URL}/projects/${params?.project_id}/classifiers/keyword_match/${params?.classifier_id}/intermediatory_class_to_keyword_configs/${params?.config_id}`,
			data
		);
		return response;
	}

	async removeKeywordClassifierConfig(params: any) {
		const response = await axios.delete(
			`${API_URL}/projects/${params?.project_id}/classifiers/keyword_match/${params?.classifier_id}/intermediatory_class_to_keyword_configs/${params?.config_id}`
		);
		return response;
	}
}
