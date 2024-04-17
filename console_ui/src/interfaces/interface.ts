export type InstanceSchema = {
	name: string;
	description: string;
	environment_slug: string;
	days_until_pi_expiration: number;
	days_until_all_data_expiration: number;
	expected_usage: string;
};
