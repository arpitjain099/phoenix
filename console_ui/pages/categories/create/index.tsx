import { MantineCreateInferencer } from "@refinedev/inferencer/mantine";
import { GetServerSideProps } from "next";

export default function CategoryCreate() {
  return <MantineCreateInferencer />;
}

export const getServerSideProps: GetServerSideProps<{}> = async (context) => {
  return {
    props: {},
  };
};
