// This file configures the initialization of Sentry on the server.
// The config you add here will be used whenever the server handles a request.
// https://docs.sentry.io/platforms/javascript/guides/nextjs/

import * as Sentry from "@sentry/nextjs";

const SENTRY_DSN = process.env.NEXT_PUBLIC_SENTRY_DSN;
const SENTRY_TRACES_SAMPLE_RATE =
	process.env.NEXT_PUBLIC_SENTRY_TRACES_SAMPLE_RATE || 1;
const SENTRY_DEBUG = process.env.NEXT_PUBLIC_SENTRY_DEBUG || false;

if (!SENTRY_DSN) {
	console.warn("NEXT_PUBLIC_SENTRY_DSN is not set");
} else {
	Sentry.init({
		dsn: SENTRY_DSN,

		// Adjust this value in production, or use tracesSampler for greater control
		tracesSampleRate: SENTRY_TRACES_SAMPLE_RATE,

		// Setting this option to true will print useful information to the console while you're setting up Sentry.
		debug: SENTRY_DEBUG,
	});
}
