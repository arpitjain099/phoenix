/* eslint-disable import/prefer-default-export */
/**
 * Formats the given date string into a human-readable date format.
 * @param {string} activeDate - The date string to be formatted.
 * @returns {string} A human-readable representation of the date.
 */
export const filterDate = (activeDate: string) => {
	const fd = new Date(activeDate);
	return fd.toDateString();
};
