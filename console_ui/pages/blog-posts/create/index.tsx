import { MantineCreateInferencer } from "@refinedev/inferencer/mantine";
import { GetServerSideProps } from "next";

export default function BlogPostCreate() {
  return <MantineCreateInferencer />;
}

export const getServerSideProps: GetServerSideProps<{}> = async (context) => {
  return {
    props: {},
  };
};
