// A faulty API route to test Sentry's error monitoring
export default function handler(_req, res) {
	throw new Error("Sentry Example API Route Error");
	// This line is unreachable, but it's here to demonstrate that the error is thrown
	// eslint-disable-next-line no-unreachable
	res.status(200).json({ name: "John Doe" });
}
