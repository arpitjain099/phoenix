"use client";

import { Modal, Button, Text } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { useEffect, useState } from "react";
import { GatherResponse } from "src/interfaces/gather";
import { jobRunService, gatherService } from "src/services";
import { formatToCurrency } from "src/utils";

interface Props {
	opened: boolean;
	setOpened: any;
	gatherDetail: any;
	handleRefresh: (value: GatherResponse) => void;
}

const GATHER_RUN_JOB_TYPE = "gather_classify_tabulate";

const GatherRunModal: React.FC<Props> = ({
	opened,
	setOpened,
	gatherDetail,
	handleRefresh,
}) => {
	const translate = useTranslate();
	const [loading, setLoading] = useState(false);
	const [estimateData, setEstimateData] = useState<any>(null);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		if (opened) {
			setLoading(true);
			gatherService
				.getGatherRunEstimate({
					project_id: gatherDetail.project_id,
					id: gatherDetail.id,
				})
				.then((response) => {
					setEstimateData(response.data);
					setLoading(false);
				})
				.catch((err) => {
					setError(err.message);
					setLoading(false);
				});
		}
	}, [opened, gatherDetail]);

	const handleClose = () => {
		setOpened(false);
		setError(null);
	};

	const handleStartRun = () => {
		setLoading(true);
		jobRunService
			.jobRun({
				project_id: gatherDetail.project_id,
				id: gatherDetail.id,
				type: GATHER_RUN_JOB_TYPE,
			})
			.then((res) => {
				handleRefresh({
					...gatherDetail,
					latest_job_run: { id: res?.data?.id },
				});
				handleClose();
				setLoading(false);
			})
			.catch((err) => {
				setError(err.message);
				setLoading(false);
			});
	};
	return (
		<Modal
			opened={opened}
			size="lg"
			onClose={() => setOpened(false)}
			withCloseButton={false}
		>
			<div className="font-medium flex flex-col px-8 pb-8">
				<h3 className="flex w-full items-center mb-6">
					<span className="font-medium text-xl">
						{translate("gathers.run_estimate.title")}
					</span>
				</h3>
				{error && <span className="text-red-500">{error}</span>}
				<div>
					<div className="mb-4">
						<Text className="uppercase text-neutral-500 font-medium text-base tracking-widest">
							{translate("gathers.details")}
						</Text>
					</div>
					<div className="w-full flex mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg capitalize">
								{gatherDetail?.source}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate("gathers.fields.source.label")}
							</Text>
						</div>
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg capitalize">
								{gatherDetail?.platform}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate("gathers.fields.platform")}
							</Text>
						</div>
					</div>
					<div className="w-full flex mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg capitalize">
								{gatherDetail?.data_type}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate("gathers.fields.data_type")}
							</Text>
						</div>
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg">
								{gatherDetail?.description}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate("gathers.fields.description")}
							</Text>
						</div>
					</div>
					<div className="mb-4">
						<Text className="mb-4 uppercase font-medium text-base tracking-widest">
							{translate("gathers.run_estimate.cost")}
						</Text>
					</div>
					<div className="w-full flex items-center mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text text-">
								{formatToCurrency(estimateData?.estimated_credit_cost)}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate("gathers.run_estimate.estimated_credit_cost")}
							</Text>
						</div>
						<div className="w-1/2 flex flex-col">
							<Text className="font-medium text-lg">
								{estimateData?.estimated_duration_minutes}
							</Text>
							<Text className="text-base text-neutral-500 font-normal">
								{translate("gathers.run_estimate.estimated_duration_minutes")}
							</Text>
						</div>
					</div>
				</div>
				<div className="flex justify-end items-center mt-4">
					<div className="flex gap-4" role="group">
						<Button variant="subtle" color="red" onClick={handleClose}>
							{translate("buttons.cancel")}
						</Button>
						<Button
							onClick={handleStartRun}
							loading={loading}
							disabled={loading}
						>
							{translate("buttons.start_run")}
						</Button>
					</div>
				</div>
			</div>
		</Modal>
	);
};

export default GatherRunModal;
