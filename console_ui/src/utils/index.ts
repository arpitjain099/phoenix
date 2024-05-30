/* eslint-disable import/prefer-default-export */
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
			return "";
	}
};

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
