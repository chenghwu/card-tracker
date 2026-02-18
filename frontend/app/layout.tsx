import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "@/lib/providers";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Card Tracker - Track Your Credit Card Benefits",
    template: "%s | Card Tracker",
  },
  description: "Smart tracking for credit card benefits with deadline alerts and usage monitoring. Never miss a benefit or deadline again.",
  keywords: ["credit card", "benefits", "tracking", "rewards", "deadline alerts", "card management"],
  authors: [{ name: "Card Tracker Team" }],
  creator: "Card Tracker",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://cardtracker.app",
    title: "Card Tracker - Track Your Credit Card Benefits",
    description: "Smart tracking for credit card benefits with deadline alerts and usage monitoring",
    siteName: "Card Tracker",
  },
  twitter: {
    card: "summary_large_image",
    title: "Card Tracker - Track Your Credit Card Benefits",
    description: "Smart tracking for credit card benefits with deadline alerts and usage monitoring",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
