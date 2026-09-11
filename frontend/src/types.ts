export type Language = 'en' | 'yo' | 'pcm' | 'ha' | 'ig';

export interface LanguageInfo {
  code: Language;
  name: string;
  nativeName: string;
  region: string;
  greeting: string;
  samplePhrase: string;
  sampleTranslation: string;
  understoodText: string;
  confirmationText: string;
  successText: string;
}

export type TransactionType = 'transfer' | 'cash_out' | 'cash_in' | 'balance';

export type TransactionStatus = 'completed' | 'pending' | 'failed';

export interface Customer {
  id: string;
  name: string;
  phone: string;
  preferredLanguage: Language;
  balance: number;
  accountNumber: string;
  bankName: string;
  faceEnrolled: boolean;
  avatar?: string;
  address?: string;
  bvnMasked: string;
}

export interface Transaction {
  id: string;
  reference: string;
  type: TransactionType;
  amount: number;
  recipient: string;
  recipientAccount?: string;
  recipientBank?: string;
  sender: string;
  date: string;
  time: string;
  status: TransactionStatus;
  language: Language;
  voiceTranscript: string;
  fee: number;
  verificationMethod: 'face_verification' | 'agent_override' | 'voice_biometric';
}

export interface Agent {
  id: string;
  name: string;
  terminalId: string;
  location: string;
  status: 'online' | 'busy' | 'offline';
  todayTransactionsCount: number;
  todayVolumeNaira: number;
  successRate: number;
}
