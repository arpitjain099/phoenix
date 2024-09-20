"use client";

import { Authenticated, CanAccess, Refine } from "@refinedev/core";
import { DevtoolsProvider } from "@refinedev/devtools";
import { RefineKbar, RefineKbarProvider } from "@refinedev/kbar";
import {
	RefineThemes,
	ThemedLayoutV2,
	ThemedTitleV2,
	useNotificationProvider,
} from "@refinedev/mantine";
import routerProvider from "@refinedev/nextjs-router";
import React, { PropsWithChildren } from "react";
import "@styles/global.css";

import {
	ColorScheme,
	ColorSchemeProvider,
	Global,
	MantineProvider,
} from "@mantine/core";
import { useLocalStorage } from "@mantine/hooks";
import { NotificationsProvider } from "@mantine/notifications";
import dataProvider from "@providers/data-provider";
import { useTranslation } from "next-i18next";

// initialize i18n
import "../providers/i18n";
import { IconUser } from "@tabler/icons";
import authProvider from "@providers/auth-provider";
import accessControlProvider from "@providers/access-provider";
import Header from "@components/header";
import Image from "next/image";

const RefineContext = ({ children }: PropsWithChildren) => {
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
								notificationProvider={useNotificationProvider}
								i18nProvider={i18nProvider}
								authProvider={authProvider}
								accessControlProvider={accessControlProvider}
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
										name: "apify_facebook_posts",
										create:
											"/projects/:projectid/gathers/apify_facebook_posts/create",
										edit: "/projects/:projectid/gathers/apify_facebook_posts/edit/:id",
										show: "/projects/:projectid/gathers/apify_facebook_posts/:id",
										meta: {
											label: "Apify Facebook Posts",
											parent: "projects",
											hide: true,
										},
									},
									{
										name: "apify_facebook_comments",
										create:
											"/projects/:projectid/gathers/apify_facebook_comments/create",
										edit: "/projects/:projectid/gathers/apify_facebook_comments/edit/:id",
										show: "/projects/:projectid/gathers/apify_facebook_comments/:id",
										meta: {
											label: "Apify Facebook Comments",
											parent: "projects",
											hide: true,
										},
									},
									{
										name: "apify_tiktok_accounts_posts",
										create:
											"/projects/:projectid/gathers/apify_tiktok_accounts_posts/create",
										edit: "/projects/:projectid/gathers/apify_tiktok_accounts_posts/edit/:id",
										show: "/projects/:projectid/gathers/apify_tiktok_accounts_posts/:id",
										meta: {
											label: "Apify Tiktok Accounts Posts",
											parent: "projects",
											hide: true,
										},
									},
									{
										name: "apify_tiktok_hashtags_posts",
										create:
											"/projects/:projectid/gathers/apify_tiktok_hashtags_posts/create",
										edit: "/projects/:projectid/gathers/apify_tiktok_hashtags_posts/edit/:id",
										show: "/projects/:projectid/gathers/apify_tiktok_hashtags_posts/:id",
										meta: {
											label: "Apify Tiktok Accounts Posts",
											parent: "projects",
											hide: true,
										},
									},
									{
										name: "apify_tiktok_comments",
										create:
											"/projects/:projectid/gathers/apify_tiktok_comments/create",
										edit: "/projects/:projectid/gathers/apify_tiktok_comments/edit/:id",
										show: "/projects/:projectid/gathers/apify_tiktok_comments/:id",
										meta: {
											label: "Apify Tiktok Comments",
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
								<Authenticated key="app">
									<CanAccess>
										<ThemedLayoutV2
											Header={() => <Header sticky />}
											Title={({ collapsed }) => (
												<ThemedTitleV2
													collapsed={collapsed}
													text="Console - Phoenix"
													icon={
														<Image
															src="/logo_buildup.png"
															width={32}
															height={32}
															alt="logo"
														/>
													}
												/>
											)}
										>
											{children}
										</ThemedLayoutV2>
									</CanAccess>
								</Authenticated>
								<RefineKbar />
							</Refine>
						</DevtoolsProvider>
					</NotificationsProvider>
				</MantineProvider>
			</ColorSchemeProvider>
		</RefineKbarProvider>
	);
};

export default RefineContext;
