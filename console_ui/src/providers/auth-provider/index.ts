import { AuthProvider } from "@refinedev/core";
import { UserInfo } from "src/interfaces/user";
import { storageService } from "src/services";

const DEV_AUTH_COOKIE = "phiphi-user-email";
const AUTH_COOKIE = process.env.NEXT_PUBLIC_AUTH_COOKIE!;
const USER_INFO_COOKIE_NAME = process.env.NEXT_PUBLIC_USER_INFO_COOKIE_NAME!;
const API_URL = process.env.NEXT_PUBLIC_API_URL!;
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
		const userData: UserInfo = await response.json();
		storageService.set(USER_INFO_COOKIE_NAME, JSON.stringify(userData));
		return userData;
	} catch (error) {
		redirectToLoginPage();
		return null;
	}
};

export const getUserRole = async (): Promise<string | null> => {
	const userInfo = storageService.get(USER_INFO_COOKIE_NAME);
	return userInfo ? JSON.parse(userInfo).app_role : null;
};

const authProvider: AuthProvider = {
	login: async () => {
		if (ENV === "dev") {
			storageService.set(DEV_AUTH_COOKIE, DEV_LOGIN_EMAIL);
		} else if (!storageService.get(AUTH_COOKIE)) {
			redirectToLoginPage();
		}
		await fetchUserInfo();
		return { success: true, redirectTo: "/" };
	},
	logout: async () => {
		storageService.remove(USER_INFO_COOKIE_NAME);
		redirectToLogoutPage();
		return { success: true };
	},
	check: async () =>
		storageService.get(AUTH_COOKIE)
			? { authenticated: true }
			: { authenticated: false, logout: true },
	getIdentity: async () => {
		const auth = storageService.get(USER_INFO_COOKIE_NAME);
		return auth ? JSON.parse(auth) : null;
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
