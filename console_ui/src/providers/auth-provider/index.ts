import { showNotification } from "@mantine/notifications";
import { AuthProvider } from "@refinedev/core";
import { UserInfo } from "src/interfaces/user";
import { storageService } from "src/services";

const DEV_AUTH_COOKIE = "phiphi-user-email";
const USER_INFO_COOKIE_NAME = process.env.NEXT_PUBLIC_USER_INFO_COOKIE_NAME!;
const API_URL = process.env.NEXT_PUBLIC_API_URL!;
const AUTH_URL = process.env.NEXT_PUBLIC_ENV_AUTH_URL!;
const AUTH_COOKIE = process.env.NEXT_PUBLIC_ENV_AUTH_COOKIE!;
const LOGIN_URL = process.env.NEXT_PUBLIC_ENV_LOGIN_URL!;
const LOGOUT_URL = process.env.NEXT_PUBLIC_ENV_LOGOUT_URL!;
const ENV = process.env.NEXT_PUBLIC_ENV!;
const DEV_LOGIN_EMAIL = process.env.NEXT_PUBLIC_DEV_ADMIN_EMAIL!;

const redirectToLoginPage = () => {
	if (ENV !== "dev" && LOGIN_URL) {
		const current_url = window.location.href;
		window.location.href = `${LOGIN_URL}?rd=${current_url}`;
	}
};

const redirectToLogoutPage = () => {
	if (ENV !== "dev" && LOGOUT_URL) {
		window.location.href = LOGOUT_URL;
	}
};

const fetchUserInfo = async (): Promise<UserInfo | null> => {
	try {
		const response = await fetch(`${API_URL}/users/me`, {
			method: "GET",
			credentials: "include",
		});
		if (!response.ok) {
			throw new Error(`HTTP error! Status: ${response.status}`);
		}
		const userData: UserInfo = await response.json();
		return userData;
	} catch (error) {
		// Handle any other errors, including network errors
		showNotification({
			title: "Error",
			message: "An error occurred while fetching user data.",
			color: "red",
		});
		return null;
	}
};

const checkAuthUrl = async (url: string): Promise<boolean> => {
	try {
		const response = await fetch(url, {
			method: "GET",
			credentials: "include",
		});
		if (response.ok) {
			return true;
		}
		return false;
	} catch (error) {
		return false;
	}
};

export const getUserRole = async (): Promise<string | null> => {
	const userInfoFromCookie = storageService.get(USER_INFO_COOKIE_NAME);
	const userInfo = userInfoFromCookie ? JSON.parse(userInfoFromCookie) : null;
	if (userInfo && Object.hasOwn(userInfo, "app_role")) {
		return userInfo.app_role;
	}
	return null;
};

const checkAuth = async (): Promise<boolean> => {
	// For this to work the cookie must not be http only
	if (AUTH_COOKIE && storageService.get(AUTH_COOKIE)) {
		return true;
	}
	if (AUTH_URL && (await checkAuthUrl(AUTH_URL))) {
		return true;
	}
	return false;
};

const authProvider: AuthProvider = {
	login: async () => {
		// Remove user info cookie so it can be refreshed after login
		storageService.remove(USER_INFO_COOKIE_NAME);
		if (ENV === "dev") {
			storageService.set(DEV_AUTH_COOKIE, DEV_LOGIN_EMAIL);
		} else {
			redirectToLoginPage();
		}
		return {
			success: false,
			error: new Error("Login failed"),
		};
	},
	logout: async () => {
		storageService.remove(USER_INFO_COOKIE_NAME);
		redirectToLogoutPage();
		return { success: true };
	},
	check: async () => {
		if (ENV === "dev" && storageService.get(DEV_AUTH_COOKIE)) {
			return { authenticated: true };
		}
		if (await checkAuth()) {
			return { authenticated: true };
		}
		return { authenticated: false };
	},
	getIdentity: async () => {
		const userInfoFromCookie = storageService.get(USER_INFO_COOKIE_NAME);
		let userInfo = null;
		if (!userInfoFromCookie) {
			userInfo = await fetchUserInfo();
			storageService.set(USER_INFO_COOKIE_NAME, JSON.stringify(userInfo));
		} else {
			userInfo = JSON.parse(userInfoFromCookie);
		}
		return userInfo;
	},
	onError: async (error) => {
		if (error.response?.status === 401) {
			redirectToLoginPage();
			return { logout: true };
		}
		return { error };
	},
};

export default authProvider;
