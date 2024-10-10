"use client";

import TypeCard from "@components/typeCard";
import { ActionIcon, Group, Title } from "@mantine/core";
import { useBack, useTranslate } from "@refinedev/core";
import {
	IconArrowLeft,
	IconBrandFacebook,
	IconBrandTiktok,
} from "@tabler/icons";
import { useParams } from "next/navigation";

export default function SelectGatherType(): JSX.Element {
	const back = useBack();
	const { projectid } = useParams();
	const translate = useTranslate();
	return (
		<div className="grow flex flex-col mt-4">
			<Group spacing="xs">
				<ActionIcon onClick={back}>
					<IconArrowLeft />
				</ActionIcon>
				<Title order={3} transform="capitalize" className="flex-1 text-center">
					{translate("gathers.titles.select_type")}
				</Title>
			</Group>
			<div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-5 mx-4 md:mx-0 justify-center mt-10 self-center">
				<TypeCard
					icon={<IconBrandFacebook className="text-blue-600" size={27} />}
					title={translate("gathers.types.apify_facebook_posts.title")}
					description={translate(
						"gathers.types.apify_facebook_posts.description"
					)}
					link={`/projects/${projectid}/gathers/apify_facebook_posts/create`}
				/>
				<TypeCard
					icon={<IconBrandFacebook className="text-blue-600" size={27} />}
					title={translate("gathers.types.apify_facebook_comments.title")}
					description={translate(
						"gathers.types.apify_facebook_comments.description"
					)}
					link={`/projects/${projectid}/gathers/apify_facebook_comments/create`}
				/>
				<TypeCard
					icon={<IconBrandTiktok className="text-blue-600" size={27} />}
					title={translate("gathers.types.apify_tiktok_accounts_posts.title")}
					description={translate(
						"gathers.types.apify_tiktok_accounts_posts.description"
					)}
					link={`/projects/${projectid}/gathers/apify_tiktok_accounts_posts/create`}
				/>
				<TypeCard
					icon={<IconBrandTiktok className="text-blue-600" size={27} />}
					title={translate("gathers.types.apify_tiktok_searches_posts.title")}
					description={translate(
						"gathers.types.apify_tiktok_searches_posts.description"
					)}
					link={`/projects/${projectid}/gathers/apify_tiktok_searches_posts/create`}
				/>
				<TypeCard
					icon={<IconBrandTiktok className="text-blue-600" size={27} />}
					title={translate("gathers.types.apify_tiktok_hashtags_posts.title")}
					description={translate(
						"gathers.types.apify_tiktok_hashtags_posts.description"
					)}
					link={`/projects/${projectid}/gathers/apify_tiktok_hashtags_posts/create`}
				/>
				<TypeCard
					icon={<IconBrandTiktok className="text-blue-600" size={27} />}
					title={translate("gathers.types.apify_tiktok_comments.title")}
					description={translate(
						"gathers.types.apify_tiktok_comments.description"
					)}
					link={`/projects/${projectid}/gathers/apify_tiktok_comments/create`}
				/>
			</div>
		</div>
	);
}
