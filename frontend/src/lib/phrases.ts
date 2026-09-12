import { Language, LanguageInfo } from '../types';
import { synthesizeSpeech } from './api';

export const LANGUAGES: Record<Language, LanguageInfo> = {
  yo: {
    code: 'yo',
    name: 'Yorùbá',
    nativeName: 'Èdè Yorùbá',
    region: 'Southwest Nigeria',
    greeting: 'Ẹ káàbọ̀ sí ElderPay',
    samplePhrase: 'Mo fẹ́ fi ẹgbàárùn-ún náírà ránṣẹ́ sí Adéwálé',
    sampleTranslation: 'I want to send 10,000 Naira to Adewale',
    understoodText: 'A ti gbọ́: Ìfipamọ́ ranṣẹ́ sí Adéwálé, ₦10,000',
    confirmationText: 'Ṣe o fẹ́ fi ẹgbàárùn-ún náírà (₦10,000) ránṣẹ́ sí Adéwálé? Jọ̀wọ́ jẹ́rìí sí i.',
    successText: 'Owó ẹgbàárùn-ún náírà ti lọ sí ọ̀dọ̀ Adéwálé pẹ̀lú àlàáfíà!'
  },
  en: {
    code: 'en',
    name: 'English',
    nativeName: 'English (Nigerian Accent)',
    region: 'Nationwide',
    greeting: 'Welcome to ElderPay',
    samplePhrase: 'Send ten thousand naira to Adewale',
    sampleTranslation: 'Send 10,000 Naira to Adewale',
    understoodText: 'Understood: Transfer ₦10,000 to Adewale',
    confirmationText: 'You are sending ten thousand naira to Adewale. Is that correct?',
    successText: 'Your transfer of ₦10,000 to Adewale was successful.'
  },
  pcm: {
    code: 'pcm',
    name: 'Nigerian Pidgin',
    nativeName: 'Naija Pidgin',
    region: 'South-South / Nationwide',
    greeting: 'How far! Welcome to ElderPay',
    samplePhrase: 'I wan send ten thousand naira give Adewale',
    sampleTranslation: 'I want to send 10,000 Naira to Adewale',
    understoodText: 'We don hear you: Transfer ₦10,000 give Adewale',
    confirmationText: 'You wan send ten thousand naira give Adewale. Make we proceed?',
    successText: 'The ten thousand naira don land for Adewale account sharp-sharp!'
  },
  ha: {
    code: 'ha',
    name: 'Hausa',
    nativeName: 'Harshen Hausa',
    region: 'Northern Nigeria',
    greeting: 'Barka da zuwa ElderPay',
    samplePhrase: 'Ina son tura naira dubu goma zuwa ga Adewale',
    sampleTranslation: 'I want to send 10,000 Naira to Adewale',
    understoodText: 'An fahimta: Canja wurin ₦10,000 zuwa Adewale',
    confirmationText: 'Kuna son tura naira dubu goma (₦10,000) zuwa ga Adewale. Haka ne?',
    successText: 'An yi nasarar tura kudi naira dubu goma zuwa ga Adewale.'
  },
  ig: {
    code: 'ig',
    name: 'Igbo',
    nativeName: 'Asụsụ Igbo',
    region: 'Southeast Nigeria',
    greeting: 'Nnọọ na ElderPay',
    samplePhrase: 'Achọrọ m iziga puku naira iri nye Adewale',
    sampleTranslation: 'I want to send 10,000 Naira to Adewale',
    understoodText: 'A ghọtara ya: Ziga ₦10,000 nye Adewale',
    confirmationText: 'Ị na-eziga puku naira iri (₦10,000) nye Adewale. Ọ bụ eziokwu?',
    successText: 'E zigara puku naira iri ahụ nye Adewale nke ọma.'
  }
};

type OnboardingPhraseKey = 'voiceEntryPrompt' | 'phoneConfirmation';

const ONBOARDING_PHRASES: Record<Language, Record<OnboardingPhraseKey, string>> = {
  en: {
    voiceEntryPrompt: 'Tap the microphone next to each box to speak your answer, or type it in.',
    phoneConfirmation: "I heard {phone}. If that's wrong, please correct it or try again."
  },
  yo: {
    voiceEntryPrompt: 'Tẹ aami gbohungbohun lẹ́gbẹ̀ẹ́ àpótí kọ̀ọ̀kan láti sọ ìdáhùn rẹ, tàbí tẹ̀ ẹ́ sínú rẹ̀.',
    phoneConfirmation: 'Mo gbọ́ {phone}. Tí kò bá tọ̀nà, jọ̀wọ́ ṣe àtúnṣe rẹ̀ tàbí tún gbìyànjú.'
  },
  pcm: {
    voiceEntryPrompt: 'Tap the microphone near each box to talk your answer, or type am inside.',
    phoneConfirmation: 'I hear {phone}. If e no correct, abeg correct am or try again.'
  },
  ha: {
    voiceEntryPrompt: 'Ta makirufo kusa da kowane akwati don faɗin amsarka, ko ka rubuta ta.',
    phoneConfirmation: 'Na ji {phone}. Idan ba daidai ba ne, don Allah ka gyara shi ko ka sake gwadawa.'
  },
  ig: {
    voiceEntryPrompt: 'Pịa igwe okwu dị n’akụkụ igbe ọ bụla iji kwuo azịza gị, ma ọ bụ pịnye ya.',
    phoneConfirmation: 'Anụla m {phone}. Ọ bụrụ na ọ bụghị eziokwu, biko mezie ya ma ọ bụ nwaa ọzọ.'
  }
};

export function getOnboardingPhrase(
  language: Language | null | undefined,
  key: OnboardingPhraseKey,
  phone?: string
): string {
  const template = ONBOARDING_PHRASES[language || 'en']?.[key] || ONBOARDING_PHRASES.en[key];
  return template.replace('{phone}', phone || '');
}

type PhraseKey =
  | 'confirmSend' | 'confirmDeposit' | 'confirmAirtime' | 'confirmWithdraw'
  | 'successSend' | 'successDeposit' | 'successAirtime' | 'successWithdraw'
  | 'welcomeBack' | 'faceAuthFailed' | 'balance'
  | 'askFullName' | 'askEmail' | 'askAddress' | 'enrollmentComplete';

const PHRASE_TEMPLATES: Record<PhraseKey, string> = {
  confirmSend: 'You are sending {0} naira to {1}. Is that correct?',
  confirmDeposit: 'You are depositing {0} naira. Is that correct?',
  confirmAirtime: 'You are buying {0} naira of airtime for {1}. Is that correct?',
  confirmWithdraw: 'You are withdrawing {0} naira. Is that correct?',
  successSend: 'Your transfer of {0} naira to {1} was successful.',
  successDeposit: 'Your deposit of {0} naira was successful.',
  successAirtime: 'Your airtime purchase of {0} naira was successful.',
  successWithdraw: 'Your withdrawal of {0} naira was successful.',
  welcomeBack: 'Welcome back, {0}.',
  faceAuthFailed: "We couldn't verify your face. Please try again.",
  balance: 'Your balance is {0} naira.',
  askFullName: 'Please enter the customer full name.',
  askEmail: 'Please enter the customer email address, or leave it blank.',
  askAddress: 'Please enter the customer address.',
  enrollmentComplete: 'Your account has been created successfully.'
};

export function phrase(language: Language, key: PhraseKey, ...values: (string | number)[]): string {
  const template = PHRASE_TEMPLATES[key] || PHRASE_TEMPLATES.faceAuthFailed;
  return template.replace(/\{(\d+)\}/g, (_, index: string) => String(values[Number(index)] ?? ''));
}

let speaking = false;
const speakingListeners = new Set<(value: boolean) => void>();

function setSpeaking(value: boolean) {
  speaking = value;
  speakingListeners.forEach((listener) => listener(value));
}

export function subscribeSpeaking(listener: (value: boolean) => void): () => void {
  speakingListeners.add(listener);
  listener(speaking);
  return () => speakingListeners.delete(listener);
}

export async function speak(text: string, language: Language): Promise<void> {
  setSpeaking(true);
  try {
    const blob = await synthesizeSpeech(text, language);
    const audio = new Audio(URL.createObjectURL(blob));
    await new Promise<void>((resolve) => {
      audio.onended = () => resolve();
      audio.onerror = () => resolve();
      void audio.play().catch(() => resolve());
    });
  } catch {
    await new Promise<void>((resolve) => {
      const completed = speakConfirmationFallback(text, resolve);
      if (!completed) resolve();
    });
  } finally {
    setSpeaking(false);
  }
}

function speakConfirmationFallback(text: string, onEnd: () => void): boolean {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return false;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.onend = onEnd;
  utterance.onerror = onEnd;
  window.speechSynthesis.speak(utterance);
  return true;
}

export function prefetchSpeech(text: string, language: Language): void {
  void synthesizeSpeech(text, language).catch(() => {});
}

export const QUICK_VOICE_COMMANDS = [
  {
    language: 'yo' as Language,
    text: 'Mo fẹ́ fi ẹgbàárùn-ún náírà ránṣẹ́ sí Adéwálé',
    translation: 'Send ₦10,000 to Adewale',
    type: 'transfer' as const,
    amount: 10000,
    recipient: 'Adewale Ogunleye'
  },
  {
    language: 'en' as Language,
    text: 'Send ten thousand naira to Adewale',
    translation: 'Send ₦10,000 to Adewale',
    type: 'transfer' as const,
    amount: 10000,
    recipient: 'Adewale Ogunleye'
  },
  {
    language: 'pcm' as Language,
    text: 'I wan withdraw five thousand naira cash',
    translation: 'Cash Out ₦5,000',
    type: 'cash_out' as const,
    amount: 5000,
    recipient: 'Self (Agent Cash)'
  },
  {
    language: 'ha' as Language,
    text: 'Duba min kudin da ke asusun na',
    translation: 'Check my account balance',
    type: 'balance' as const,
    amount: 0,
    recipient: 'Account Balance'
  },
  {
    language: 'ig' as Language,
    text: 'Achọrọ m itinye puku naira iri abụọ n’akpa ego m',
    translation: 'Cash In ₦20,000 deposit',
    type: 'cash_in' as const,
    amount: 20000,
    recipient: 'Adewale Ogunleye (Self)'
  }
];
