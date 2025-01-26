import { PropsWithChildren } from "react";

export function Layout({ children }: PropsWithChildren) {
  return <div className="flex min-h-screen flex-col p-4">{children}</div>;
}
