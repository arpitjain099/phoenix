"use client";

import { ScrollArea, Table } from "@mantine/core";
import React, { useEffect, useState } from "react";
import { useTranslate } from "@refinedev/core";
import { GatherResponse } from "src/interfaces/gather";
import GatherRow from "@components/project/gather-row";
import Pagination from "./pagination";

const GatherTable: React.FC<{
	data: any[];
	setSelected: any;
	setOpened: any;
	setDeleteModalOpen: any;
}> = ({ data, setSelected, setOpened, setDeleteModalOpen }) => {
	const translate = useTranslate();
	const [dataSource, setDataSource] = useState<any[]>([]);
	const [pages, setPages] = useState<number>(1);
	const [activeIndex, setActiveIndex] = useState<number>(1);

	useEffect(() => {
		if (data) {
			const allData = data;
			const pageSize = 10;
			const currentPageData = allData.slice(
				(activeIndex - 1) * pageSize,
				activeIndex * pageSize
			);

			setDataSource(currentPageData);
			setPages(Math.ceil(allData.length / pageSize));
		}
	}, [activeIndex, data]);
	return (
		<>
			<ScrollArea>
				<Table highlightOnHover>
					<thead>
						<tr>
							<th>{translate("gathers.fields.name")}</th>
							<th>{translate("gathers.fields.started_run_at")}</th>
							<th>{translate("gathers.fields.completed_at")}</th>
							<th>{translate("projects.fields.status")}</th>
							<th>{translate("table.actions")}</th>
						</tr>
					</thead>
					<tbody>
						{dataSource.map((gather: GatherResponse) => (
							<GatherRow
								key={gather.id}
								row={gather}
								setSelected={setSelected}
								setOpened={setOpened}
								setDeleteModalOpen={setDeleteModalOpen}
								translate={translate}
							/>
						))}
					</tbody>
				</Table>
			</ScrollArea>
			<br />
			<Pagination
				pages={pages}
				_activeIndex={activeIndex}
				_setActiveIndex={setActiveIndex}
			/>
		</>
	);
};

export default GatherTable;
