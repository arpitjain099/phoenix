/* eslint-disable import/prefer-default-export */

import { JobRunResponse } from "src/interfaces/job-run";

/**
 * Formats the given date string into a human-readable date format.
 * @param {string} date - The date string to be formatted.
 * @returns {string} A human-readable representation of the date.
 */
export const toReadableDate = (date: string): string => {
	const fd = new Date(date);
	return fd.toDateString();
};

export const statusTextStyle = (type: any): string => {
	switch (type) {
		case "awaiting_start":
			return "text-orange-500";
		case "in_queue":
			return "text-orange-500";
		case "processing":
			return "text-orange-500";
		case "failed":
			return "text-red-500";
		case "completed_sucessfully":
			return "text-green-500";
		default:
			return "text-neutral-500";
	}
};

export const isJobRunRunning = (jobRun: JobRunResponse | null): boolean =>
	jobRun !== null && !jobRun.completed_at;

export const formatToCurrency = (value: number | string): string => {
	let numberValue: number;

	if (typeof value === "string") {
		numberValue = parseFloat(value);
	} else {
		numberValue = value;
	}

	// Check if the value is a valid number
	if (Number.isNaN(numberValue)) {
		return "0";
	}
	if (!numberValue) {
		return "0";
	}

	return numberValue.toLocaleString("en-US", {
		style: "decimal",
		minimumFractionDigits: 0,
		maximumFractionDigits: 2,
	});
};

export const PHEONIX_MANUAL_URL =
	"https://docs.google.com/document/d/1Rs3WYgvkAtZJ9y1ho68AnGfC8mDuOFE9aG52bkJSG24/edit";
