import { ErrorComponent } from "@refinedev/mantine";
import { GetServerSideProps } from "next";

export default function CatchAll() {
	return <ErrorComponent />;
}

export const getServerSideProps: GetServerSideProps<{}> = async (_context) => ({
	props: {},
});
