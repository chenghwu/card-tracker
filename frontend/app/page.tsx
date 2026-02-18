import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CreditCard, TrendingUp, Bell, CheckCircle } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <CreditCard className="h-6 w-6" />
            <span className="text-xl font-bold">Card Tracker</span>
          </div>
          <nav className="flex items-center gap-4">
            <Button variant="ghost" asChild>
              <Link href="/login">Sign In</Link>
            </Button>
            <Button asChild>
              <Link href="/login">Get Started</Link>
            </Button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container py-24 md:py-32">
        <div className="mx-auto max-w-3xl text-center">
          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
            Never Miss a Credit Card Benefit Again
          </h1>
          <p className="mt-6 text-lg leading-8 text-muted-foreground">
            Track your credit card benefits, credits, and perks with smart deadline alerts.
            Maximize your rewards and never lose money on unused benefits.
          </p>
          <div className="mt-10 flex items-center justify-center gap-4">
            <Button size="lg" asChild>
              <Link href="/login">Start Tracking Free</Link>
            </Button>
            <Button size="lg" variant="outline" asChild>
              <Link href="#features">Learn More</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="container py-24">
        <div className="mx-auto max-w-5xl">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Smart Benefit Tracking
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Everything you need to maximize your credit card benefits
            </p>
          </div>

          <div className="mt-16 grid gap-8 md:grid-cols-2">
            <Card>
              <CardHeader>
                <Bell className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>Smart Deadline Alerts</CardTitle>
                <CardDescription>
                  Color-coded alerts for expiring benefits. Red for critical (≤3 days),
                  orange for warning (≤7 days), yellow for upcoming (≤14 days).
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <TrendingUp className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>Track Usage & Progress</CardTitle>
                <CardDescription>
                  Visual progress bars show how much you've used. Record partial usage
                  and see exactly what's remaining.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CreditCard className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>All Your Cards in One Place</CardTitle>
                <CardDescription>
                  Manage multiple credit cards with monthly, quarterly, semi-annual,
                  and annual benefits. Supports both calendar year and membership year tracking.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CheckCircle className="h-8 w-8 mb-2 text-primary" />
                <CardTitle>Comprehensive Dashboard</CardTitle>
                <CardDescription>
                  See your total annual fees, benefit value, and net value at a glance.
                  Track which benefits need attention right now.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container py-24">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="text-3xl font-bold tracking-tight">
            Ready to maximize your credit card benefits?
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Start tracking your cards for free. No credit card required.
          </p>
          <div className="mt-8">
            <Button size="lg" asChild>
              <Link href="/login">Get Started Now</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container text-center text-sm text-muted-foreground">
          <p>&copy; 2026 Card Tracker. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
