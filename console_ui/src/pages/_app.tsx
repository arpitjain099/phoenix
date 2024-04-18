import { Refine } from "@refinedev/core";
import { DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";
import {
	RefineThemes,
	ThemedLayoutV2,
	ThemedTitleV2,
	notificationProvider,
} from "@refinedev/mantine";
import routerProvider, {
	DocumentTitleHandler,
	UnsavedChangesNotifier,
} from "@refinedev/nextjs-router";
import React, { useEffect, useState } from "react";
import type { NextPage } from "next";
import { AppProps } from "next/app";
import "@styles/global.css";

import Header from "@components/header";
import {
	ColorScheme,
	ColorSchemeProvider,
	Global,
	MantineProvider,
	Skeleton,
} from "@mantine/core";
import { useLocalStorage } from "@mantine/hooks";
import { NotificationsProvider } from "@mantine/notifications";
import dataProvider from "@providers/data-provider";
import { appWithTranslation, useTranslation } from "next-i18next";

// initialize i18n
import "../providers/i18n";
import { IconUser } from "@tabler/icons";
import { useRouter } from "next/router";
import authProvider from "@providers/auth-provider";

export type NextPageWithLayout<P = {}, IP = P> = NextPage<P, IP> & {
	noLayout?: boolean;
};

type AppPropsWithLayout = AppProps & {
	Component: NextPageWithLayout;
};

function MyApp({ Component, pageProps }: AppPropsWithLayout): JSX.Element {
	const router = useRouter();
	const [loading, setLoading] = useState(true);
	const renderComponent = () => {
		if (Component.noLayout) {
			return <Component {...pageProps} />;
		}

		return (
			<ThemedLayoutV2
				Header={() => <Header sticky />}
				Title={({ collapsed }) => (
					<ThemedTitleV2 collapsed={collapsed} text="Console UI" />
				)}
			>
				<Component {...pageProps} />
			</ThemedLayoutV2>
		);
	};

	const { t, i18n } = useTranslation();

	const i18nProvider = {
		translate: (key: string, params: object) => t(key, params),
		changeLocale: (lang: string) => i18n.changeLanguage(lang),
		getLocale: () => i18n.language,
	};

	const [colorScheme, setColorScheme] = useLocalStorage<ColorScheme>({
		key: "mantine-color-scheme",
		defaultValue: "light",
		getInitialValueInEffect: true,
	});
	const toggleColorScheme = (value?: ColorScheme) =>
		setColorScheme(value || (colorScheme === "dark" ? "light" : "dark"));

	useEffect(() => {
		const checkAuth = async () => {
			const { authenticated } = await authProvider.check();
			if (!authenticated) {
				await authProvider.login({});
			}
			setLoading(false);
		};
		checkAuth();
	}, [router]);

	if (loading) {
		return <Skeleton />; // Show a loading indicator while checking authentication
	}

	return (
		<RefineKbarProvider>
			<ColorSchemeProvider
				colorScheme={colorScheme}
				toggleColorScheme={toggleColorScheme}
			>
				{/* You can change the theme colors here. example: theme={{ ...RefineThemes.Magenta, colorScheme:colorScheme }} */}
				<MantineProvider
					theme={{ ...RefineThemes.Blue, colorScheme }}
					withNormalizeCSS
					withGlobalStyles
				>
					<Global styles={{ body: { WebkitFontSmoothing: "auto" } }} />
					<NotificationsProvider position="top-right">
						<DevtoolsProvider>
							<Refine
								routerProvider={routerProvider}
								dataProvider={dataProvider}
								notificationProvider={notificationProvider}
								i18nProvider={i18nProvider}
								authProvider={authProvider}
								resources={[
									{
										name: "projects",
										list: "/projects",
										create: "/projects/create",
										edit: "/projects/edit/:id",
										show: "/projects/show/:id",
										meta: {
											canDelete: true,
										},
									},
									{
										name: "",
										list: "/projects/:projectid/gathers",
										create: "/projects/:projectid/gathers/create",
										meta: {
											label: "Gathers",
											parent: "projects",
											hide: true,
										},
									},
									{
										name: "profile",
										list: "/profile",
										meta: {
											label: "Profile",
											icon: <IconUser size="16" />,
										},
									},
								]}
								options={{
									syncWithLocation: true,
									warnWhenUnsavedChanges: true,
									useNewQueryKeys: true,
									projectId: "nMl5vA-MzwgF4-ONcYky",
								}}
							>
								{renderComponent()}
								<RefineKbar />
								<UnsavedChangesNotifier />
								<DocumentTitleHandler />
							</Refine>
						</DevtoolsProvider>
					</NotificationsProvider>
				</MantineProvider>
			</ColorSchemeProvider>
		</RefineKbarProvider>
	);
}

export default appWithTranslation(MyApp);
