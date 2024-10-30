"use client";

import { Table } from "@mantine/core";
import React from "react";

const TableWithChildComponent: React.FC<{ children: React.ReactNode }> = ({
	children,
}) => <Table>{children}</Table>;

export default TableWithChildComponent;
