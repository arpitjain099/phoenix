import { MantineEditInferencer } from "@refinedev/inferencer/mantine";
import { GetServerSideProps } from "next";

export default function InstancesEdit() {
  return <MantineEditInferencer />;
}

export const getServerSideProps: GetServerSideProps<{}> = async (context) => {
  return {
    props: {},
  };
};
