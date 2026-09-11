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

export type Action = "send" | "balance" | "withdraw" | "deposit" | "airtime" | "bill" | "unknown";
export type TransactionType = 'transfer' | 'cash_out' | 'cash_in' | 'balance';

export type TransactionState =
  | "INTENT_DETECTED"
  | "COLLECTING_DETAILS"
  | "CONFIRMATION_REQUIRED"
  | "USER_CONFIRMED"
  | "FACE_VERIFICATION_REQUIRED"
  | "FACE_VERIFIED"
  | "TRANSACTION_PROCESSING"
  | "TRANSACTION_SUCCESS"
  | "USER_CANCELLED"
  | "INVALID_AMOUNT"
  | "INSUFFICIENT_FUNDS"
  | "UNKNOWN_RECIPIENT"
  | "LOW_AI_CONFIDENCE"
  | "TRANSACTION_FAILED"
  | "FACE_VERIFICATION_FAILED"
  | "PAYMENT_API_ERROR";

export interface ParsedIntent {
  action: Action;
  amount: number | null;
  recipient: string | null;
  confidence: number;
}

export interface TransactionRecord {
  id: string;
  userId: string;
  action: Action;
  amount: number | null;
  recipient: string | null;
  recipientAccount: string | null;
  confidence: number | null;
  state: TransactionState;
  createdAt: string;
  faceVerified: boolean;
  verificationMethod?: "face" | "voice" | null;
  paymentReference: string | null;
  error: string | null;
  needsClarification?: "amount" | "recipient" | "accountNumber";
}

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
  code: string;
  terminalId?: string;
  location?: string;
  status?: 'online' | 'busy' | 'offline';
  todayTransactionsCount?: number;
  todayVolumeNaira?: number;
  successRate?: number;
}

export interface HealthStatus {
  ok: boolean;
  demoMode: boolean;
  paystackConfigured: boolean;
  dbConnected: boolean;
}

export interface AgentPayoutProfile {
  paystackRecipientCode: string | null;
  paystackAccountNumber: string | null;
  paystackBankCode: string | null;
  payoutOnboarded: boolean;
}
export type Language = 'en' | 'yo' | 'pcm' | 'ha' | 'ig';

<<<<<<< HEAD
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
=======
export type TransactionState =
  | "INTENT_DETECTED"
  | "COLLECTING_DETAILS"
  | "CONFIRMATION_REQUIRED"
  | "USER_CONFIRMED"
  | "FACE_VERIFICATION_REQUIRED"
  | "FACE_VERIFIED"
  | "TRANSACTION_PROCESSING"
  | "TRANSACTION_SUCCESS"
  | "USER_CANCELLED"
  | "INVALID_AMOUNT"
  | "INSUFFICIENT_FUNDS"
  | "UNKNOWN_RECIPIENT"
  | "LOW_AI_CONFIDENCE"
  | "TRANSACTION_FAILED"
  | "FACE_VERIFICATION_FAILED"
  | "PAYMENT_API_ERROR";

export interface ParsedIntent {
  action: Action;
  amount: number | null;
  recipient: string | null;
  confidence: number;
}

export interface TransactionRecord {
  id: string;
  userId: string;
  action: Action;
  amount: number | null;
  recipient: string | null;
  recipientAccount: string | null;
  confidence: number | null;
  state: TransactionState;
  createdAt: string;
  faceVerified: boolean;
  verificationMethod?: "face" | "voice" | null;
  paymentReference: string | null;
  error: string | null;
  needsClarification?: "amount" | "recipient" | "accountNumber";
}
>>>>>>> 75f2459 (Replace BMONI withdrawals with Paystack transfers)

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
<<<<<<< HEAD
  terminalId: string;
  location: string;
  status: 'online' | 'busy' | 'offline';
  todayTransactionsCount: number;
  todayVolumeNaira: number;
  successRate: number;
=======
  code: string;
}

export interface HealthStatus {
  ok: boolean;
  demoMode: boolean;
  paystackConfigured: boolean;
  dbConnected: boolean;
}

export interface AgentPayoutProfile {
  paystackRecipientCode: string | null;
  paystackAccountNumber: string | null;
  paystackBankCode: string | null;
  payoutOnboarded: boolean;
>>>>>>> 75f2459 (Replace BMONI withdrawals with Paystack transfers)
}
