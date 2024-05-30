import React, { useEffect, useState, useMemo, useCallback } from "react";
import {
	IResourceComponentsProps,
	useTranslate,
	useList,
} from "@refinedev/core";
import { useTable } from "@refinedev/react-table";
import { ColumnDef } from "@tanstack/react-table";
import {
	ScrollArea,
	Pagination,
	Group,
	Button,
	Tooltip,
	Loader,
} from "@mantine/core";
import { DateField, List } from "@refinedev/mantine";
import TableComponent from "@components/table";
import { useRouter } from "next/router";
import BreadcrumbsComponent from "@components/breadcrumbs";
import { statusTextStyle } from "src/utils";
import { IconRefresh, IconTrash } from "@tabler/icons";
import { jobRunService } from "src/services";
import { JobRunResponse } from "src/interfaces/job-run";

export const TabulateList: React.FC<IResourceComponentsProps> = () => {
	const translate = useTranslate();
	const router = useRouter();
	const { projectid } = router.query || {};
	const [loading, setLoading] = useState(false);
	const [tabulateList, setTabulateList] = useState<any>([]);
	const [loadingStates, setLoadingStates] = useState<{
		[key: string]: boolean;
	}>({});

	const breadcrumbs = [
		{ title: translate("projects.projects"), href: "/projects" },
		{ title: translate("tabulate.tabulate"), href: "#" },
	];

	const apiResponse = useList({
		resource: projectid
			? `projects/${projectid}/job_runs?foreign_job_type=tabulate`
			: "",
		pagination: { mode: "off" },
	});

	const handleRefresh = useCallback(
		async (jobDetail: JobRunResponse) => {
			setLoadingStates((prev) => ({ ...prev, [jobDetail.id]: true }));
			try {
				const { data } = await jobRunService.fetchJobRun({
					project_id: Number(projectid),
					id: jobDetail?.id,
					type: "tabulate",
				});
				setTabulateList((prevList: JobRunResponse[]) =>
					prevList.map((job) =>
						job.id === jobDetail.id ? { ...job, latest_job_run: data } : job
					)
				);
			} catch (error) {
				console.error("Error fetching gather details:", error);
			} finally {
				setLoadingStates((prev) => ({ ...prev, [jobDetail.id]: false }));
			}
		},
		[projectid]
	);

	const columns = useMemo<ColumnDef<any>[]>(
		() => [
			{
				id: "started_processing_at",
				accessorKey: "started_processing_at",
				header: translate("tabulate.fields.started_processing_at"),
				cell: ({ getValue }) =>
					getValue() ? <DateField value={getValue<any>()} /> : "",
			},
			{
				id: "completed_at",
				accessorKey: "completed_at",
				header: translate("tabulate.fields.completed_at"),
				cell: ({ getValue }) =>
					getValue() ? <DateField value={getValue<any>()} /> : "",
			},
			{
				id: "status",
				accessorKey: "status",
				header: translate("projects.fields.status"),
				cell: ({ getValue }) => {
					const status = getValue() || "";
					return <span className={statusTextStyle(status)}>{`${status}`}</span>;
				},
			},
			{
				id: "actions",
				accessorKey: "id",
				header: translate("table.actions"),
				cell: ({ row }) => {
					const gatherId = row.original.id;
					const { status } = row.original;
					const isLoading = loadingStates[gatherId];
					return (
						<Group spacing="xs" noWrap>
							{isLoading ? (
								<Loader size="sm" />
							) : (
								<>
									{(status === "in_queue" || status === "processing") && (
										<Tooltip label="Refresh">
											<Button
												p={0}
												variant="subtle"
												onClick={() => handleRefresh(row.original)}
											>
												<IconRefresh size={20} color="blue" />
											</Button>
										</Tooltip>
									)}
									{["failed", "completed_sucessfully"].includes(status) && (
										<Button
											p={0}
											variant="subtle"
											color="red"
											onClick={() => {}}
										>
											<IconTrash
												size={20}
												color="red"
												className="cursor-pointer"
											/>
										</Button>
									)}
								</>
							)}
						</Group>
					);
				},
			},
		],
		[translate, loadingStates, handleRefresh]
	);

	const {
		getHeaderGroups,
		getRowModel,
		setOptions,
		refineCore: { setCurrent, pageCount, current },
	} = useTable({
		columns,
		data: tabulateList,
	});

	setOptions((prev) => ({
		...prev,
		meta: { ...prev.meta },
	}));

	useEffect(() => {
		if (apiResponse?.data?.data) {
			setTabulateList(apiResponse.data.data);
		}
	}, [apiResponse?.data?.data]);

	const handleStartRun = () => {
		setLoading(true);
		jobRunService
			.gatherRun({
				project_id: Number(projectid),
				id: 0,
				type: "tabulate",
			})
			.then((res) => {
				handleRefresh(res.data);
				setLoading(false);
			})
			.catch((err) => {
				console.log("err", err);
				setLoading(false);
			});
	};

	return (
		<List
			canCreate={false}
			breadcrumb={<BreadcrumbsComponent breadcrumbs={breadcrumbs} />}
			headerButtons={({ defaultButtons }) => (
				<>
					{defaultButtons}
					<Button type="button" loading={loading} onClick={handleStartRun}>
						Run a tabulate
					</Button>
				</>
			)}
		>
			<ScrollArea>
				<TableComponent
					headerGroups={getHeaderGroups}
					rowModel={getRowModel}
					data={apiResponse}
				/>
			</ScrollArea>
			<br />
			<Pagination
				position="right"
				total={pageCount}
				page={current}
				onChange={setCurrent}
			/>
		</List>
	);
};

export default TabulateList;
