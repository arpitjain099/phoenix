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
