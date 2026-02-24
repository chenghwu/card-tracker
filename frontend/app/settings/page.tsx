'use client';

import { useState, useEffect } from 'react';
import { MainLayout } from '@/components/layout/main-layout';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Switch } from '@/components/ui/switch';
import { Separator } from '@/components/ui/separator';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { User, Bell, LogOut, Mail } from 'lucide-react';

export default function SettingsPage() {
  const [email, setEmail] = useState('demo@example.com');
  const [name, setName] = useState('');
  const [expiringBenefits, setExpiringBenefits] = useState(true);
  const [weeklySummary, setWeeklySummary] = useState(false);

  // Pull email from localStorage if available (e.g. stored after OAuth)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('user_email');
      if (stored) setEmail(stored);
      const storedName = localStorage.getItem('user_name');
      if (storedName) setName(storedName);
    }
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_email');
    window.location.href = '/login';
  };

  return (
    <MainLayout>
      <div className="space-y-6 max-w-2xl">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
          <p className="text-muted-foreground">
            Manage your account and preferences
          </p>
        </div>

        {/* Section 1: Account */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="h-5 w-5" />
              Account
            </CardTitle>
            <CardDescription>Your account information</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {name && (
              <div className="space-y-1">
                <Label className="text-xs text-muted-foreground uppercase tracking-wide">
                  Name
                </Label>
                <p className="text-sm font-medium">{name}</p>
              </div>
            )}
            <div className="space-y-1">
              <Label className="text-xs text-muted-foreground uppercase tracking-wide">
                Email
              </Label>
              <p className="text-sm font-medium">{email}</p>
            </div>

            <Separator />

            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Sign out</p>
                <p className="text-xs text-muted-foreground">
                  Clears your session and redirects to login
                </p>
              </div>
              <Button variant="outline" onClick={handleSignOut} size="sm">
                <LogOut className="h-4 w-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Section 2: Notifications */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Notifications
            </CardTitle>
            <CardDescription>
              Control how you are notified about your benefits
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <Alert>
              <Mail className="h-4 w-4" />
              <AlertDescription>
                Email notification settings will take effect once email is configured
              </AlertDescription>
            </Alert>

            <div className="flex items-center justify-between gap-4">
              <div className="space-y-0.5">
                <Label htmlFor="expiring-benefits" className="text-sm font-medium">
                  Email reminders for expiring benefits
                </Label>
                <p className="text-xs text-muted-foreground">
                  Get notified when a benefit is about to expire
                </p>
              </div>
              <Switch
                id="expiring-benefits"
                checked={expiringBenefits}
                onCheckedChange={setExpiringBenefits}
              />
            </div>

            <Separator />

            <div className="flex items-center justify-between gap-4">
              <div className="space-y-0.5">
                <Label htmlFor="weekly-summary" className="text-sm font-medium">
                  Weekly summary email
                </Label>
                <p className="text-xs text-muted-foreground">
                  A digest of your benefit usage and upcoming deadlines each week
                </p>
              </div>
              <Switch
                id="weekly-summary"
                checked={weeklySummary}
                onCheckedChange={setWeeklySummary}
              />
            </div>
          </CardContent>
        </Card>

        {/* Section 3: Display — placeholder for future use */}
        <Card>
          <CardHeader>
            <CardTitle>Display</CardTitle>
            <CardDescription>
              Display preferences will be available in a future update
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">Nothing to configure here yet.</p>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
