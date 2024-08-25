"use client";

import TypeCard from "@components/typeCard";
import { useTranslate } from "@refinedev/core";
import { IconBrandFacebook, IconBrandTiktok } from "@tabler/icons";
import { useParams } from "next/navigation";

export default function SelectGatherType(): JSX.Element {
	const { projectid } = useParams();
	const translate = useTranslate();
	return (
		<div className="grow flex flex-col mt-4">
			<div className="w-full text-center text-ap-grey-950 font-semibold text-2xl">
				Select the type of gather you would like to do
			</div>
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
			</div>
		</div>
	);
}
