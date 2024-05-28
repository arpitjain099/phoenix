import { Modal, Button } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import { useEffect, useState } from "react";
import { GatherResponse } from "src/interfaces/gather";
import { gatherService } from "src/services";
import { formatToCurrency } from "src/utils";

interface Props {
	opened: boolean;
	setOpened: any;
	gatherDetail: any;
	handleRefresh: (value: GatherResponse) => void;
}

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
					gather_id: gatherDetail.id,
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
		gatherService
			.gatherRun({
				project_id: gatherDetail.project_id,
				gather_id: gatherDetail.id,
				type: "gather",
			})
			.then(() => {
				handleRefresh(gatherDetail);
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
						<span className="uppercase text-neutral-800 font-medium text-xs tracking-widest">
							{translate("gathers.details")}
						</span>
					</div>
					<div className="w-full flex mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<span className="text-neutral-800 font-medium text-sm capitalize">
								{gatherDetail?.source}
							</span>
							<span className="text-xs text-neutral-500 font-normal">
								{translate("gathers.fields.source")}
							</span>
						</div>
						<div className="w-1/2 flex flex-col">
							<span className="text-neutral-800 font-medium text-sm capitalize">
								{gatherDetail?.platform}
							</span>
							<span className="text-xs text-neutral-500 font-normal">
								{translate("gathers.fields.platform")}
							</span>
						</div>
					</div>
					<div className="w-full flex mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<span className="text-neutral-800 font-medium text-sm capitalize">
								{gatherDetail?.data_type}
							</span>
							<span className="text-xs text-neutral-500 font-normal">
								{translate("gathers.fields.data_type")}
							</span>
						</div>
						<div className="w-1/2 flex flex-col">
							<span className="text-neutral-800 font-medium text-sm">
								{gatherDetail?.description}
							</span>
							<span className="text-xs text-neutral-500 font-normal">
								{translate("gathers.fields.description")}
							</span>
						</div>
					</div>
					<div className="mb-4">
						<span className="mb-4 uppercase text-neutral-800 font-medium text-xs tracking-widest">
							{translate("gathers.run_estimate.cost")}
						</span>
					</div>
					<div className="w-full flex items-center mb-5 p-1">
						<div className="w-1/2 flex flex-col">
							<span className="text-neutral-800 font-medium text-sm">
								{formatToCurrency(estimateData?.estimated_credit_cost)}
							</span>
							<span className="text-xs text-neutral-500 font-normal">
								{translate("gathers.run_estimate.estimated_credit_cost")}
							</span>
						</div>
						<div className="w-1/2 flex flex-col">
							<span className="text-neutral-800 font-medium text-sm">
								{estimateData?.estimated_duration_minutes}
							</span>
							<span className="text-xs text-neutral-500 font-normal">
								{translate("gathers.run_estimate.estimated_duration_minutes")}
							</span>
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
