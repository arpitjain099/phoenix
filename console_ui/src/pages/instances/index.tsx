import { MantineListInferencer } from "@refinedev/inferencer/mantine";
import { GetServerSideProps } from "next";

export default function InstancesList() {
	return <MantineListInferencer />;
}

export const getServerSideProps: GetServerSideProps<{}> = async (_context) => ({
	props: {},
});
