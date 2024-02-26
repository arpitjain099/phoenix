import { MantineCreateInferencer } from "@refinedev/inferencer/mantine";
import { GetServerSideProps } from "next";

export default function InstancesCreate() {
	return <MantineCreateInferencer />;
}

export const getServerSideProps: GetServerSideProps<{}> = async (_context) => ({
	props: {},
});
