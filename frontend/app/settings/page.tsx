'use client';

import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
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
import { Skeleton } from '@/components/ui/skeleton';
import { User, Bell, LogOut } from 'lucide-react';
import { toast } from 'sonner';
import { getPreferences, updatePreferences } from '@/lib/api';

export default function SettingsPage() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const queryClient = useQueryClient();

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedEmail = localStorage.getItem('user_email');
      if (storedEmail) setEmail(storedEmail);
      const storedName = localStorage.getItem('user_name');
      if (storedName) setName(storedName);
    }
  }, []);

  const { data: prefs, isLoading } = useQuery({
    queryKey: ['preferences'],
    queryFn: getPreferences,
  });

  const mutation = useMutation({
    mutationFn: updatePreferences,
    onSuccess: (data) => {
      queryClient.setQueryData(['preferences'], data);
      toast.success('Preferences saved');
    },
    onError: () => toast.error('Failed to save preferences'),
  });

  const handleSignOut = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_name');
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

        {/* Account */}
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
                <Label className="text-xs text-muted-foreground uppercase tracking-wide">Name</Label>
                <p className="text-sm font-medium">{name}</p>
              </div>
            )}
            {email && (
              <div className="space-y-1">
                <Label className="text-xs text-muted-foreground uppercase tracking-wide">Email</Label>
                <p className="text-sm font-medium">{email}</p>
              </div>
            )}
            <Separator />
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Sign out</p>
                <p className="text-xs text-muted-foreground">Clears your session and redirects to login</p>
              </div>
              <Button variant="outline" onClick={handleSignOut} size="sm">
                <LogOut className="h-4 w-4 mr-2" />
                Sign Out
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Notifications */}
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
            {isLoading ? (
              <div className="flex items-center justify-between">
                <div className="space-y-1.5">
                  <Skeleton className="h-4 w-48" />
                  <Skeleton className="h-3 w-64" />
                </div>
                <Skeleton className="h-6 w-10 rounded-full" />
              </div>
            ) : (
              <div className="flex items-center justify-between gap-4">
                <div className="space-y-0.5">
                  <Label htmlFor="email-reminders" className="text-sm font-medium">
                    Email reminders for expiring benefits
                  </Label>
                  <p className="text-xs text-muted-foreground">
                    Get notified at 7, 3, and 1 day before a benefit expires
                  </p>
                </div>
                <Switch
                  id="email-reminders"
                  checked={prefs?.email_reminders_enabled ?? true}
                  disabled={mutation.isPending}
                  onCheckedChange={(checked) =>
                    mutation.mutate({ email_reminders_enabled: checked })
                  }
                />
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
