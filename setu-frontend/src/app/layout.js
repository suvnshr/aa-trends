import { DM_Sans } from "next/font/google";
import "./globals.css";

// Meta data of the website
export const metadata = {
  title: "Setu - AA trends",
  description: "Trends of AA",
};

const dmSansFont = DM_Sans({ subsets: ["latin"] })

// Root layout
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        // Use DM Sans(google font) for the website
        className={dmSansFont.className}>{children}</body>
    </html>
  );
}
