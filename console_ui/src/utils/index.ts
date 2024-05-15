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
    case "in_queue":
      return "text-orange-500";
		case "not_yet_run":
			return "text-orange-500";
    case "processing":
      return "text-orange-500";
    case "failed":
      return "text-red-500";
    case "completed":
      return "text-green-500";
    default:
      return "";
  }
}

