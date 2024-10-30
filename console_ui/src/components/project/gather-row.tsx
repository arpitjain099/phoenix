// GatherRow.tsx
import React, { useState, useCallback, useEffect } from "react";
import { Group, Button, Tooltip, Loader } from "@mantine/core";
import { DateField } from "@refinedev/mantine";
import { IconPlayerPlay, IconTrash } from "@tabler/icons";
import Link from "next/link";
import { isJobRunRunning, statusTextStyle } from "src/utils";
import { GatherResponse } from "src/interfaces/gather";
import { jobRunService } from "src/services";

interface GatherRowProps {
	row: GatherResponse;
	setSelected: React.Dispatch<React.SetStateAction<any>>;
	setOpened: React.Dispatch<React.SetStateAction<boolean>>;
	setDeleteModalOpen: React.Dispatch<React.SetStateAction<boolean>>;
	translate: (key: string) => string;
}

const GatherRow: React.FC<GatherRowProps> = ({
	row,
	setSelected,
	setOpened,
	setDeleteModalOpen,
	translate,
}) => {
	const { id, name, child_type, project_id } = row;

	// Initialize local state with data from props
	const [latestJobRun, setLatestJobRun] = useState(row.latest_job_run);
	const [deleteJobRun, setDeleteJobRun] = useState(row.delete_job_run);
	const [isLoading, setIsLoading] = useState(false);

	// Update local state when props change
	useEffect(() => {
		setLatestJobRun(row.latest_job_run);
		setDeleteJobRun(row.delete_job_run);
	}, [row.latest_job_run, row.delete_job_run]);

	// Use effect to refresh pending gathers at intervals
	useEffect(() => {
		let interval: NodeJS.Timeout | undefined;
		const isPending =
			(latestJobRun && !latestJobRun.completed_at) ||
			(deleteJobRun && !deleteJobRun.completed_at);

		if (isPending) {
			interval = setInterval(() => {
				handleGatherRefresh();
			}, 10000);
		}
		return () => {
			if (interval) {
				clearInterval(interval);
			}
		};
	}, [latestJobRun, deleteJobRun, handleGatherRefresh]);

	const status = latestJobRun ? latestJobRun.status : null;

	return (
		<tr>
			<td>
				<Link
					href={`/projects/${project_id}/gathers/${child_type}/${id}`}
					className="no-underline text-blue-500"
				>
					{name}
				</Link>
			</td>
			<td>
				{latestJobRun?.started_processing_at ? (
					<span
						className={`${
							deleteJobRun?.status === "completed_successfully"
								? statusTextStyle("deleted")
								: ""
						}`}
					>
						<DateField
							format="LLL"
							value={latestJobRun.started_processing_at}
						/>
					</span>
				) : (
					""
				)}
			</td>
			<td>
				{latestJobRun?.completed_at ? (
					<span
						className={`${
							deleteJobRun?.status === "completed_successfully"
								? statusTextStyle("deleted")
								: ""
						}`}
					>
						<DateField format="LLL" value={latestJobRun.completed_at} />
					</span>
				) : (
					""
				)}
			</td>
			<td>
				<span
					className={`${statusTextStyle(
						deleteJobRun?.status === "completed_successfully"
							? "deleted"
							: deleteJobRun?.status
								? deleteJobRun?.status
								: status
					)}`}
				>
					{deleteJobRun
						? translate(`status.delete_status.${deleteJobRun.status}`)
						: status
							? translate(`status.${status}`)
							: ""}
				</span>
			</td>
			<td>
				<Group spacing="xs" noWrap>
					{isLoading ? (
						<Loader size="sm" />
					) : (
						<>
							{!status && (
								<Tooltip label="Start">
									<Button
										p={0}
										variant="subtle"
										color="green"
										onClick={() => {
											setSelected(row);
											setOpened(true);
										}}
									>
										<IconPlayerPlay size={20} color="green" />
									</Button>
								</Tooltip>
							)}
							{(isJobRunRunning(latestJobRun) ||
								isJobRunRunning(deleteJobRun)) && <Loader size="sm" />}
							{latestJobRun?.completed_at &&
								!isJobRunRunning(deleteJobRun) &&
								deleteJobRun?.status !== "completed_successfully" && (
									<Tooltip label="Delete">
										<Button
											p={0}
											variant="subtle"
											color="red"
											onClick={() => {
												setSelected(row);
												setDeleteModalOpen(true);
											}}
										>
											<IconTrash size={20} color="red" />
										</Button>
									</Tooltip>
								)}
						</>
					)}
				</Group>
			</td>
		</tr>
	);
};

export default GatherRow;
