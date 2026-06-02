import AppHeader from "./AppHeader";

export default function BrandHeader({ title = "SiteSpy", subtitle, compact = false }) {
  return (
    <AppHeader
      logo
      centered={!compact}
      kicker="SiteSpy"
      title={title}
      subtitle={subtitle}
    />
  );
}
