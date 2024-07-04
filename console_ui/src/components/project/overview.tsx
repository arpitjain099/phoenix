"use client";

import { Anchor, Checkbox, Text, Title } from "@mantine/core";
import { useTranslate } from "@refinedev/core";
import Link from "next/link";
import React from "react";

interface IOverviewProps {
	setActiveTab: any;
}

const OverviewComponent: React.FC<IOverviewProps> = ({ setActiveTab }) => {
	const translate = useTranslate();
	return (
		<div className="p-4">
			<Title order={3}>{translate("projects.tabs.overview.title")}</Title>

			<Text fz="sm" c="dimmed">
				{translate("projects.tabs.overview.description.part1.a")}
				<span className="font-bold">
					{translate("projects.tabs.overview.description.part1.b")}
				</span>
			</Text>
			<Text fz="sm" c="dimmed" mt={10}>
				{translate("projects.tabs.overview.description.part2.a")}
				<Anchor
					className="underline underline-offset-1"
					href="https://docs.google.com/document/d/1Rs3WYgvkAtZJ9y1ho68AnGfC8mDuOFE9aG52bkJSG24/edit"
					target="_blank"
				>
					{translate("projects.tabs.overview.description.part2.b")}
				</Anchor>
			</Text>
			<Text fz="sm" c="dimmed" mt={10}>
				{translate("projects.tabs.overview.description.part3")}
			</Text>
			<div className="my-2 relative z-10">
				<ul className="my-0 px-0 text-left font-medium text-lg leading-none border-blue-200 divide-y divide-blue-200">
					<div>
						<Link
							className="py-3.5 w-full flex items-center text-blue-500 hover:text-blue-700 hover:bg-blue-50 no-underline"
							href="https://docs.google.com/document/d/1Rs3WYgvkAtZJ9y1ho68AnGfC8mDuOFE9aG52bkJSG24/edit"
							target="_blank"
						>
							{/* <span className="ml-5 mr-2.5 w-1 h-7 bg-blue-500 rounded-r-md" /> */}
							<Checkbox checked={false} mr="md" />
							{translate("projects.tabs.overview.problem_statement")}
							<span className="ml-1 font-normal text-gray-500 text-sm">
								({translate("projects.tabs.overview.tips.manual")})
							</span>
						</Link>
					</div>
					<div>
						<Link
							className="py-3.5 w-full flex items-center text-blue-500 hover:text-blue-700 hover:bg-blue-50 no-underline"
							href="https://docs.google.com/document/d/1Rs3WYgvkAtZJ9y1ho68AnGfC8mDuOFE9aG52bkJSG24/edit"
							target="_blank"
						>
							<Checkbox checked={false} mr="md" />
							Define where you will get data from
							<span className="ml-1 font-normal text-gray-500 text-sm">
								({translate("projects.tabs.overview.tips.manual")})
							</span>
						</Link>
					</div>
					<div>
						<div
							className="py-3.5 w-full flex items-center text-blue-500 hover:text-blue-700 hover:bg-blue-50 cursor-pointer"
							onClick={() => setActiveTab("gather")}
							aria-hidden="true"
						>
							<Checkbox checked={false} mr="md" />
							{translate("projects.tabs.overview.gather")}
							<span className="ml-1 font-normal text-gray-500 text-sm">
								({translate("projects.tabs.overview.tips.gather")})
							</span>
						</div>
					</div>
					<div>
						<div
							className="py-3.5 w-full flex items-center text-blue-500 hover:text-blue-700 hover:bg-blue-50 cursor-pointer"
							onClick={() => setActiveTab("classify")}
							aria-hidden="true"
						>
							<Checkbox checked={false} mr="md" />
							{translate("projects.tabs.overview.classify")}
							<span className="ml-1 font-normal text-gray-500 text-sm">
								({translate("projects.tabs.overview.tips.classify")})
							</span>
						</div>
					</div>
					<div>
						<div
							className="py-3.5 w-full flex items-center text-blue-500 hover:text-blue-700 hover:bg-blue-50 cursor-pointer"
							onClick={() => setActiveTab("visualise")}
							aria-hidden="true"
						>
							<Checkbox checked={false} mr="md" />
							{translate("projects.tabs.overview.visualise")}
							<span className="ml-1 font-normal text-gray-500 text-sm">
								({translate("projects.tabs.overview.tips.visualise")})
							</span>
						</div>
					</div>
					<div>
						<Link
							className="py-3.5 w-full flex items-center text-blue-500 hover:text-blue-700 hover:bg-blue-50 no-underline"
							href="https://docs.google.com/document/d/1Rs3WYgvkAtZJ9y1ho68AnGfC8mDuOFE9aG52bkJSG24/edit"
							target="_blank"
						>
							<Checkbox checked={false} mr="md" />
							{translate("projects.tabs.overview.insights")}
							<span className="ml-1 font-normal text-gray-500 text-sm">
								({translate("projects.tabs.overview.tips.manual")})
							</span>
						</Link>
					</div>
				</ul>
			</div>
		</div>
	);
};

export default OverviewComponent;
