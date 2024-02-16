import { MantineShowInferencer } from "@refinedev/inferencer/mantine";
import { GetServerSideProps } from "next";

export default function CategoryShow() {
  return <MantineShowInferencer />;
}

export const getServerSideProps: GetServerSideProps<{}> = async (context) => {
  return {
    props: {},
  };
};
