import { Suspense } from "react";

import { NavigateToResource } from "@refinedev/nextjs-router";
import { Authenticated } from "@refinedev/core";

export default function Home() {
	return (
		<Suspense>
			<Authenticated key="home-page">
				<NavigateToResource resource="projects" />;
			</Authenticated>
		</Suspense>
	);
}

Home.noLayout = true;
