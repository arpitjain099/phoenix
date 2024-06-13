import { useTranslate } from "@refinedev/core";
import { Button } from "@mantine/core";
import { IconEye } from "@tabler/icons";
import Link from "next/link";

interface DashboardLinkButtonProps {
	environmentSlug: string;
	platformDomainBase?: string;
	platformSchemaBase?: string;
}

const PLATFORM_DOMAIN_BASE = process.env.NEXT_PUBLIC_PLATFORM_DOMAIN_BASE!;
const PLATFORM_SCHEMA_BASE = process.env.NEXT_PUBLIC_PLATFORM_SCHEMA_BASE!;

const DashboardLinkButton: React.FC<DashboardLinkButtonProps> = ({
	environmentSlug,
	platformDomainBase = PLATFORM_DOMAIN_BASE || "",
	platformSchemaBase = PLATFORM_SCHEMA_BASE || "",
}) => {
	const translate = useTranslate();

	if (!platformDomainBase || !platformSchemaBase) {
		return null;
	}

	const href = `${platformSchemaBase}://dashboard.${environmentSlug}.${platformDomainBase}`;

	return (
		<Link href={href} target="_blank">
			<Button leftIcon={<IconEye />}>
				{translate("projects.titles.dashboard")}
			</Button>
		</Link>
	);
};

export default DashboardLinkButton;
