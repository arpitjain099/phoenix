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
	Title,
	Text,
} from "@mantine/core";
import { DateField, List } from "@refinedev/mantine";
import TableComponent from "@components/table";
import { useRouter } from "next/router";
import BreadcrumbsComponent from "@components/breadcrumbs";
import { statusTextStyle } from "src/utils";
import { IconRefresh } from "@tabler/icons";
import { jobRunService } from "src/services";
import { JobRunResponse } from "src/interfaces/job-run";
import { GetServerSideProps } from "next";

export const getServerSideProps: GetServerSideProps<{}> = async (_context) => ({
	props: {},
});

const TabulateList: React.FC<IResourceComponentsProps> = () => {
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
		{ title: projectid as string, href: `/projects/show/${projectid}` },
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
					prevList.map((job) => (job.id === jobDetail.id ? data : job))
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
				id: "created_at",
				accessorKey: "created_at",
				header: translate("gathers.fields.started_run_at"),
				cell: ({ getValue }) =>
					getValue() ? <DateField format="LLL" value={getValue<any>()} /> : "",
			},
			{
				id: "started_processing_at",
				accessorKey: "started_processing_at",
				header: translate("tabulate.fields.started_processing_at"),
				cell: ({ getValue }) =>
					getValue() ? <DateField format="LLL" value={getValue<any>()} /> : "",
			},
			{
				id: "completed_at",
				accessorKey: "completed_at",
				header: translate("tabulate.fields.completed_at"),
				cell: ({ getValue }) =>
					getValue() ? <DateField format="LLL" value={getValue<any>()} /> : "",
			},
			{
				id: "status",
				accessorKey: "status",
				header: translate("projects.fields.status"),
				cell: ({ getValue }) => {
					const status = getValue() || "";
					return (
						<span className={`${statusTextStyle(status)}`}>
							{status ? translate(`status.${status}`) : ""}
						</span>
					);
				},
			},
			{
				id: "actions",
				accessorKey: "id",
				header: translate("table.actions"),
				cell: ({ row }) => {
					const jobId = row.original.id;
					const { status } = row.original;
					const isLoading = loadingStates[jobId];
					return (
						<Group spacing="xs" noWrap>
							{isLoading ? (
								<Loader size="sm" />
							) : (
								["in_queue", "processing"].includes(status) && (
									<Tooltip label="Refresh">
										<Button
											p={0}
											variant="subtle"
											onClick={() => handleRefresh(row.original)}
										>
											<IconRefresh size={20} color="blue" />
										</Button>
									</Tooltip>
								)
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
			.jobRun({
				project_id: Number(projectid),
				id: 0,
				type: "tabulate",
			})
			.then(() => {
				apiResponse.refetch();
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
			title={
				<div className="flex flex-col">
					<Title order={3}>{translate("tabulate.title")}</Title>
					<Text fz="sm" c="dimmed">
						{translate("tabulate.sub_titles.list")}
					</Text>
				</div>
			}
			headerButtons={({ defaultButtons }) => (
				<>
					{defaultButtons}
					<Button
						type="button"
						loading={loading}
						onClick={handleStartRun}
						disabled={tabulateList.some(
							(item: JobRunResponse) => item.completed_at === null
						)}
					>
						{translate("tabulate.run")}
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
