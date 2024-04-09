/* eslint-disable import/prefer-default-export */
export const filterDate = (activeDate: string) => {
	const fd = new Date(activeDate);
	return fd.toDateString();
};
