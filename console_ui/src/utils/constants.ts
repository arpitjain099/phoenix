/* eslint-disable import/prefer-default-export */

import { FormValidationResult } from "@mantine/form/lib/types";
import { SetStateAction } from "react";

// Handle Gather Save
export const handleGatherSave = async (
	resource: string,
	redirectRoute: string,
	isValid: any,
	projectid: string,
	setLoading: (value: SetStateAction<boolean>) => void,
	mutate: any,
	formValues: any,
	setInputList: (value: SetStateAction<string[]>) => void,
	reset: () => void,
	router: any,
	validate: () => FormValidationResult,
	id?: string
) => {
	if (isValid()) {
		if (projectid) {
			setLoading(true);
			mutate(
				{
					resource,
					id,
					values: formValues,
					errorNotification: (res: any) => {
						let message = "Something went wrong while creating";
						if (res?.response?.data?.detail[0]?.msg) {
							message = res.response.data.detail[0].msg;
						}
						return {
							message,
							description: "Error",
							type: "error",
						};
					},
				},
				{
					onSuccess: async () => {
						await Promise.all([setInputList([]), reset()]);
						setTimeout(() => {
							router.push(redirectRoute);
						}, 1000);
					},
					onError: () => {
						setLoading(false);
					},
				}
			);
		}
	} else {
		validate();
	}
};
